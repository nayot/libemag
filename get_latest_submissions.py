import os
import re
import sys

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python script.py <directory>")

    directory = sys.argv[1]
    process_submissions(directory)

def process_submissions(directory):
    # Group 1: Student ID (8 digits)
    # Group 2: Assignment Name
    # Group 3: Version number (optional)
    pattern = re.compile(r"(\d{8})[_-](\w+)(?: ?\((\d+)\))?\.ipynb")

    # Dictionary to store ALL files per student ID to determine which is newest
    # Format: { 'student_id': [ {'path': path, 'mtime': time, 'name': name}, ... ] }
    student_records = {}

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            student_id = match.group(1)
            file_path = os.path.join(directory, filename)
            mod_time = os.path.getmtime(file_path)

            if student_id not in student_records:
                student_records[student_id] = []
            
            student_records[student_id].append({
                'full_path': file_path,
                'filename': filename,
                'mod_time': mod_time
            })

    for student_id, files in student_records.items():
        # Sort files by modification time (descending)
        # The first item [0] will be the latest
        files.sort(key=lambda x: x['mod_time'], reverse=True)
        
        latest_file = files[0]
        older_files = files[1:]

        # 1. Handle the Latest File
        official_name = f"{student_id}.ipynb"
        official_path = os.path.join(directory, official_name)
        
        if latest_file['filename'] != official_name:
            os.rename(latest_file['full_path'], official_path)
            print(f"LATEST: {latest_file['filename']} -> {official_name}")
        else:
            print(f"LATEST: {official_name} is already correct.")

        # 2. Handle Older Files
        for old in older_files:
            # Prevent double-prefixing if script is run twice
            if not old['filename'].startswith("OLD_"):
                old_official_name = f"OLD_{old['filename']}"
                old_official_path = os.path.join(directory, old_official_name)
                os.rename(old['full_path'], old_official_path)
                print(f"ARCHIVED: {old['filename']} -> {old_official_name}")

if __name__ == "__main__":
    main()
