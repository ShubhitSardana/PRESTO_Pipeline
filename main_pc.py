import os
import subprocess
import shutil
import chardet
import logging
from decimal import Decimal

# Logging Function
logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

# ----Basic Functions---- #

# create directory
def create_directory(directory_path):
    logging.info('Executing create_directory function')
    try:
        os.mkdir(directory_path)
        print("Directory created successfully.")
    except OSError as e:
        print("Directory creation failed:", e)


# moving files to a directory
def move_files_to_dir(source_dir, target_dir, extension):
    logging.info('Executing move_files_to_dir function')
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    # Get a list of files with the specified extension in the source directory
    files_to_move = [file for file in os.listdir(source_dir) if file.endswith(extension)]
    
    for file in files_to_move:
        source_file = os.path.join(source_dir, file)
        target_file = os.path.join(target_dir, file)
        
        try:
            shutil.move(source_file, target_file)
            print(f"Moved {file} to {target_dir}")
        except Exception as e:
            print(f"Failed to move {file}: {e}")


# to get the name of filterbank file
def get_filenames(directory, n):
    logging.info('Executing get_filenames function')
    txt_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.fil'):
                txt_files.append(file)
    return txt_files[n]


# reading config data
def read_config_data(option):
    logging.info('Executing read_config_data function')
    # Open the file
    with open("./config.txt", "r") as file:
        # Read the contents of the file
        contents = file.read()

        # Search for the line that contains "option"
        for line in contents.split('\n'):
            if option in line:
                # Extract the value from the line
                value = line.split('=')[-1].strip()
                break
        else:
            # Handle the case where the line is not found
            value = None
        
        return value
    

# Replace word in dedisp file
def replace_word_in_file(input_path, output_path, word, replacement_word):
    logging.info('Executing replace_word_in_file')
    try:
        # Read the content of the input file
        with open(input_path, "r") as input_file:
            file_content = input_file.read()

        # Replace occurrences of the search word with the replacement word
        modified_content = file_content.replace(word, replacement_word)

        # Write the modified content to the new file
        with open(output_path, "w") as output_file:
            output_file.write(modified_content)

        print("Word '{}' replaced with '{}' and saved in '{}'.".format(word, replacement_word, output_path))

    except FileNotFoundError:
        print("File not found: '{}'.".format(input_path))
    except Exception as e:
        print("An error occurred:", str(e))


# ----PRESTO Commands---- #

# rficlean
def rficlean():
    logging.info('Executing rficlean')
    filename = get_filenames("./", 0)
    command = f"rficlean -o {filename[0:-4:1]}_clean.fil {filename}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)


# ddplan 
def ddplan():
    logging.info('Executing ddplan')
    try:
        n = read_config_data("Number of channels")
        b = read_config_data("Total Bandwidth")
        t = read_config_data("Sample time")
        f = read_config_data("Central freq")
        s = read_config_data("Number of Subbands")
        filename = get_filenames("./", 1)
        # Create the command with the current pair of files
        command = ['DDplan.py','-d', '1000', '-n', f'{n}', '-b', f'{b}', '-t', f'{t}', '-f', f'{f}', '-s', f'{s}', '-w', f'{filename[::1]}']

        # Run the command
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process.communicate(b'\n')
        process.wait()

    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)        


# dedisp
def dedisp():
    logging.info('Executing dedisp')
    try:
        filename = get_filenames("./", 1)
        replace_word_in_file(f"./dedisp_{filename[0:-4:1]}.py", "./dedisp.py", "prepsubband", "prepsubband -nobary")
        command = f"python3 dedisp.py"    
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)


# realfft
def realfft():
    logging.info('Executing run_realfft')
    command = "realfft *.dat"
 
    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)


# accelsearch
def accelsearch():
    logging.info('Executing run_accelsearch')
    command = "ls *.fft | xargs -n 1 accelsearch"
 
    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)
# run_accelsearch()


# changing encoding <In-between process> to correct encoding for accelsift to not show an error
def change_encoding(file_extension):
    logging.info('Executing change_encoding')
    directory = "./"
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath) and filename.endswith(file_extension):
            try:
                with open(filepath, 'rb') as file:
                    content = file.read()
                    result = chardet.detect(content)
                    encoding = result['encoding']
                
                with open(filepath, 'r', encoding=encoding, errors='replace') as file:
                    content = file.read()
                
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                print(f"File '{filename}' converted from '{encoding}' to UTF-8 encoding.")
            
            except UnicodeDecodeError:
                print(f"Error decoding file '{filename}'. Skipping the file.")
                continue
            except Exception as e:
                print(f"Error occurred while converting file '{filename}': {str(e)}")
                continue


# accelsift
def accelsift():
    logging.info('Executing accelsift')
    command = "python3 /data1/mpsurnis/soft/presto/examplescripts/ACCEL_sift.py" 

    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)


# prepfold <jut to viauslise the data>
def prepfold(cand_dir, dat_dir):
    logging.info('Executing prepfold')
    # Get the list of .cand and .dat files in the directories
    cand_files = [f for f in os.listdir(cand_dir) if f.endswith('.cand')]

    # Iterate over the files and run prepfold on each pair

    i = Decimal('0.00')
    increment = Decimal('0.10')
    for cand_file in cand_files:
        filename = get_filenames("./", 1)
        # Create the command with the current pair of files
        command = ['prepfold', '-topo', '-accelcand', '1', '-accelfile', os.path.join(cand_dir, cand_file), filename, '-o', f"{filename}_DM_{i}"]

        # Run the command
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process.communicate(b'\n')
        process.wait()
        i = i + increment
        

def clean_all():
    logging.info('Executing clean_all function')
    try:
        # prepsubband files
        move_files_to_dir("./", "./prepsubband_output", ".inf")
        move_files_to_dir("./", "./prepsubband_output", ".dat")
        move_files_to_dir("./", "./prepsubband_output/realfft_output", ".fft")
        # candidate files
        move_files_to_dir("./", "./candidate_files", "00")
        move_files_to_dir("./", "./candidate_files", ".cand")
        move_files_to_dir("./", "./candidate_files", ".txtcand") 
        # RFIClean files
        move_files_to_dir("./", "./rficlean_output", "clean.fil")
        move_files_to_dir("./", "./rficlean_output", "rficlean_output.pdat")
        move_files_to_dir("./", "./rficlean_output/ps_output", "rficlean_output.ps")
        # prepfold output
        move_files_to_dir("./", "./prepfold_output", ".pfd")
        move_files_to_dir("./", "./prepfold_output/postscript", ".pfd.ps")
        move_files_to_dir("./", "./prepfold_output", "pfd.bestprof")

    except Exception as e:
        pass


# ---- Function Calling---- #

if __name__ == "__main__":
    try:
        logging.info('Starting program execution')
        rficlean()
        ddplan()
        dedisp()
        realfft()
        accelsearch()
        change_encoding("_200")
        accelsift()
        prepfold("./", "./")
        clean_all()
        logging.info('Program executed successfully')
    except Exception as e:
        logging.exception('An error occurred: ' + str(e))