import os
from jedi import directory
from jedi_functions import dir_search_file

"""

This script is called by jedi.py in case the --d flag is specified.
The user has given a directory name, that holds the files with the redundant internal coordinates. 

"""

# Initializing variables for search in specified data folder
ba_state = False
bl_state = False
da_state = False

if directory:
    print("Starting jedi_directory.py, as --d flag is specified.") 
    directory_check = os.path.isdir(directory)

    if not directory_check: # there is no directory w/ specified name.
        print(f"\t There is no directory \"{directory}\", so I'm creating one.")
        os.makedirs(directory)

    elif directory_check: 
        if not os.listdir(directory):  # there is a directory w/ specified name, but it's empty.
            print(f"\t There is a directory called \"{directory}\", but it's empty. Carrying out JEDI-Analysis in this folder..")

        elif os.listdir(directory):  # there is a directory w/ specified name and there are files in there.

            # check which of the necessary files are in there.
            __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
            os.chdir(__dirpath__)

            # bl.txt, ba.txt and da.txt
            bl_state = dir_search_file(directory, 'bl.txt')
            ba_state = dir_search_file(directory, 'ba.txt')
            da_state = dir_search_file(directory, 'da.txt')

    __origpath__ = os.path.dirname(os.getcwd())
    os.chdir(__origpath__)

if not ba_state:
    ba_state = False
if not bl_state:
    bl_state = False
if not da_state:
    da_state = False
