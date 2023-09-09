import os
import subprocess


def execute_main_in_subdirs(directory):
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            os.chdir(subdir_path)
            if os.path.exists("main.py"):
                try:
                    subprocess.run(["python3", "main.py"], check=True)
                    print("main.py executed in", subdir_path)
                except subprocess.CalledProcessError as e:
                    print("Execution of main.py failed in", subdir_path)
                    print("Error:", e)
            else:
                print("main.py does not exist in", subdir_path)
            os.chdir("../")


# Calling the function to run the command in each directory
execute_main_in_subdirs("./")
