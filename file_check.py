from pathlib import Path
import re
import nbformat

def main():
    # Get path to files
    file_path = input("Enter path to files (such as C:\\Downloads\\): ")

    # Convert to path object
    path = Path(file_path)

    # Check filenames of all files in the directory
    invalid_filenames, invalid_meta = check_all_files_in_directory(path)

    # Display checking results
    if len(invalid_filenames) == 0:
        print("All filenames are valid!")
    else:
        print("The following filenames are NOT valid")
        for file in invalid_filenames:
            print(file)
    if len(invalid_meta) == 0:
        print("All files contain metadata")
    else:
        print("The following files DO NOT contain metadata:")
        for file in invalid_meta:
            print(file)


def check_filename(filename):
    pattern = r"\d{8}_\w+.ipynb"
    match = re.search(pattern, filename)
    if match:
        return True
    else:
        return False

from pathlib import Path

def check_all_files_in_directory(directory):
    invalid_filenames = []
    invalid_meta = []
    
    # Iterate through all files in the directory
    for file in directory.iterdir():
        if file.is_file():  # Ensure it's a file
            if not check_filename(file.name):
                invalid_filenames.append(file.name)
            if not find_nbgrader_metadata(file):
                invalid_meta.append(file.name)

    return invalid_filenames, invalid_meta

# Function to check for cell metadata containing a specific keyword
def find_nbgrader_metadata(file_path):
    try:
        # Open the Jupyter notebook file
        with open(file_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # Loop through the cells to check for 'nbgrader' in metadata
        for idx, cell in enumerate(notebook.cells):
            if "metadata" in cell and "nbgrader" in cell.metadata:
                # print(f"Cell {idx + 1} contains 'nbgrader' metadata:")
                # print(cell.metadata["nbgrader"])
                # print("Metadata found! Your file is good ...")
                return True

        return False

    except Exception as e:
        print(f"Error reading the notebook file: {e}")


if __name__ == "__main__":
    main()