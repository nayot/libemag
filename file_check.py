from pathlib import Path
import re
import nbformat
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def main():
    messages = "" # Messages to be displayed as output

    if len(sys.argv) < 2:
        # Get path to files
        #file_path = input("Enter path to files (such as C:\\Downloads\\): ")
        file_path = select_path()
        if not file_path: # Wrong input given
            messages = "Wrong selection!\n"
            show_result(messages)
            return 0 
    else:
        file_path = sys.argv[1]

    # Convert to path object
    path = Path(file_path)

    # Check filenames of all files in the directory
    invalid_filenames, invalid_meta = check_all_files_in_directory(path)

    # Display checking results
    if len(invalid_filenames) == 0:
        # print("Filename(s) valid!!")
        messages += "Filename(s) valid!!\n"
    else:
        #print("The following filename(s) NOT valid")
        messages += "The following filename(s) NOT valid\n"
        for file in invalid_filenames:
            #print(file)
            messages += (file + "\n")

    if len(invalid_meta) == 0:
        # print("Metadata found!!")
        messages += "Metadata found!!\n"
    else:
        # print("The following file(s) DO NOT contain metadata:")
        messages += "The following file(s) DO NOT contain metadata:\n" 
        for file in invalid_meta:
            # print(file)
            messages += (file + "\n")

    show_result(messages)


def select_path():
    """
    Opens a dialog to select either a file or a directory.
    Returns the selected path (file or directory).
    """
    selected_path = {"path": None}  # A mutable container to store the selection

    def select_file():
        selected_path["path"] = filedialog.askopenfilename(title="Select a File")
        root.quit()  # Close the GUI after selection

    def select_directory():
        selected_path["path"] = filedialog.askdirectory(title="Select a Directory")
        root.quit()  # Close the GUI after selection

    # Create the main GUI window
    root = tk.Tk()
    root.title("Select File or Directory")

    # Add a label to display instructions
    label = tk.Label(root, text="Choose to select a file or a directory.", wraplength=400)
    label.pack(pady=10)

    # Add a button to select a file
    file_button = tk.Button(root, text="Select File", command=select_file)
    file_button.pack(pady=5)

    # Add a button to select a directory
    dir_button = tk.Button(root, text="Select Directory", command=select_directory)
    dir_button.pack(pady=5)

    # Run the application
    root.mainloop()

    # Return the selected path
    return selected_path["path"]

def show_result(text):
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Check Result", text)

def check_filename(filename):
    pattern = r"^(62|63|64|65|66|67)\d{6}.ipynb"
    match = re.search(pattern, filename)
    if match:
        return True
    else:
        return False

from pathlib import Path

def check_all_files_in_directory(directory):
    invalid_filenames = []
    invalid_meta = []

    # Check if it's a file or directory
    if directory.is_dir():    
        # Iterate through all files in the directory
        num_file = 0
        for file in directory.iterdir():
            num_file += 1
            if file.is_file():  # Ensure it's a file
                if not check_filename(file.name):
                    invalid_filenames.append(file.name)
                if not find_nbgrader_metadata(file):
                    invalid_meta.append(file.name)
    else: # It's just a file
        file = directory
        num_file = 1
        if not check_filename(file.name):
            invalid_filenames.append(file.name)
        if not find_nbgrader_metadata(file):
            invalid_meta.append(file.name)

    if num_file == 0:
        show_result("No files found!!")
        sys.exit(0)

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
