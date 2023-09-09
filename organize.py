import os
import shutil


def organize_files(directory):
    # Get the list of files with .fil extension in the directory
    files = [file for file in os.listdir(directory) if file.endswith('.fil')]

    # Create a folder for each file and move the file into that folder
    for file in files:
        # Extract the filename without the extension
        filename = os.path.splitext(file)[0]

        # Create a folder with the same name as the filename
        folder_path = os.path.join(directory, filename)
        os.makedirs(folder_path, exist_ok=True)

        # Move the file into the created folder
        file_path = os.path.join(directory, file)
        shutil.move(file_path, folder_path)

    print("Files organized successfully.")

def copy_main_file_to_directories(directory):
    main_file_path = "main.py"
    config_file_path = "config.txt"
    for root, dirs, files in os.walk(directory):
        # Copy the main.py file to each directory
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            shutil.copy(main_file_path, dir_path)
            shutil.copy(config_file_path, dir_path)
    print("main.py and config.txt copied to directories successfully. Make changes to config.txt as per requirement.")



# Calling Functions
organize_files("./")
copy_main_file_to_directories("./")


