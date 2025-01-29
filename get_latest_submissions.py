import os
import re
import sys

def main():
    # Verify the directory
    if len(sys.argv) != 2:
        sys.exit("Invalid argument")

    directory = sys.argv[1]
    get_latest_submissions(directory)

def get_latest_submissions(directory):
    # Regular expression to match filenames like 65050123_ic01.ipynb
    pattern = re.compile(r"(\d{8}_\w+)(?: ?\((\d+)\))?\.ipynb")

    # Debug
#    for filename in os.listdir(directory):
#        match = pattern.match(filename)
#        file_path = os.path.join(directory, filename)
#        file_mod_time = os.path.getmtime(file_path)  # Get file modification time
#
#        if match:
#            print(match.group(1), match.group(2), file_mod_time)
#    return

    # Dictionary to store the latest file for each student ID
    latest_files = {}

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            student_id = match.group(1)
            file_path = os.path.join(directory, filename)
            file_mod_time = os.path.getmtime(file_path)  # Get file modification time

            if student_id not in latest_files or latest_files[student_id]['mod_time'] < file_mod_time:
                latest_files[student_id] = {'filename': filename, 'mod_time': file_mod_time}

    # Process the latest files
    for student_id, file_info in latest_files.items():
        current_filename = file_info['filename']
        official_filename = f"{student_id}.ipynb"
        current_path = os.path.join(directory, current_filename)
        official_path = os.path.join(directory, official_filename)

        # Rename the latest file to the official filename format
        if current_filename != official_filename:
            os.rename(current_path, official_path)
            print(f"Renamed: {current_filename} -> {official_filename}")
        else:
            print(f"File already correct: {official_filename}")
if __name__ == "__main__":
    main()