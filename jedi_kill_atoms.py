import re
import sys
import numpy as np
import os
import jedi_files
from jedi_functions import search_line, read_xyz
from jedi_directory import directory, bl_state, ba_state, da_state

"""

This script is called by jedi.py

It reads jedi_kill_atoms_input.txt to generate list of to be deleted atoms. 
It deletes atoms from Hessian (H_Cart.txt), and geometry-files (x0.txt and xF.txt).

"""

with open("jedi_kill_atoms_input.txt") as file:

    # relaxed geometry 
    input_line = search_line("Enter atom numbers to delete in relaxed geometry here:", file)
    file.seek(0)
    file = file.readlines()

    ls_NrAtoms = [] # list containing to be deleted in relaxed geometry

    for i in range(input_line, len(file)):
        if re.match('[0-9]', file[i]):
            NrAtoms = file[i].split("\n")
            ls_NrAtoms.append(int(NrAtoms[0]))
        elif file[i].startswith("##"):
            break

    # strained geometry 
    strained_input_line = search_line("Enter atom numbers to delete in strained geometry here:", file)

    strained_ls_NrAtoms = [] # list containing to be deleted in relaxed geometry

    for i in range(strained_input_line, len(file)):
        if re.match('[0-9]', file[i]):
            NrAtoms = file[i].split("\n")
            strained_ls_NrAtoms.append(int(NrAtoms[0]))

print("Starting jedi_kill_atoms.py to check if atoms specified, that should be ignored in JEDI-Calculation.")

# Check if highest proposed atom numbers exists in relaxed molecule: 
if len(ls_NrAtoms) == 0: 
    print("\t INFO: No user input in jedi_kill_atoms_input.txt, so no atoms are ignored in JEDI-Calculation.")
elif int(max(ls_NrAtoms)) > int(jedi_files.NAtoms):
    print("\t ERROR: Highest to be deleted atom number is", max(ls_NrAtoms), "while there are only", jedi_files.NAtoms, "atoms in the molecule.")
    print("\t Please check the user input in jedi_kill_atoms_input.txt")
    print("\t I am stopping jedi.py now.")
    sys.exit()


# ############### script to delete atoms starts here ####################
# #######################################################################     

if len(strained_ls_NrAtoms) != 0:

    # xF
    with open("xF.txt") as xF:
        xF.seek(0)
        xF_lines = xF.readlines()

        if os.path.exists("xF_manip.txt"):
            os.remove("xF_manip.txt")

        with open("xF_manip.txt", "a") as xF_manip: 
            print(jedi_files.NAtoms, "\n", file = xF_manip)

            xF_strained_ls_NrAtoms = [x+1 for x in strained_ls_NrAtoms] # add one to accomodate first two rows not containing coordinates
            # list starts at one, while python counts from 0 - only add one although need to skip two rows

            for i in range(2, len(xF_lines)):
                if not (int(i) in xF_strained_ls_NrAtoms):
                    print(xF_lines[i], end='', file = xF_manip)
    xF.close()
    xF_manip.close()
    # os.remove("xF.txt") 

if len(ls_NrAtoms) != 0:

   # x0

    with open("x0.txt") as x0:
        x0.seek(0)
        x0_lines = x0.readlines()
        
        if os.path.exists("x0_manip.txt"):
            os.remove("x0_manip.txt")
        
        with open("x0_manip.txt", "a") as x0_manip:
            print(jedi_files.NAtoms, "\n", file = x0_manip)

            x0_ls_NrAtoms = [x+1 for x in ls_NrAtoms] # see xF_strained_ls_NrAtoms

            for i in range(2, len(x0_lines)): # start at 2 to skip first two rows containing atom number
                if not (int(i) in x0_ls_NrAtoms):
                    print(x0_lines[i], end='', file=x0_manip)
    x0.close()
    x0_manip.close()
    os.remove("x0.txt") 

    # bl
    if bl_state == True: 
        __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
        os.chdir(__dirpath__)

    with open("bl.txt") as bl: 
        bl.seek(0)
        bl = bl.readlines()
        if os.path.exists("bl_manip.txt"):
            os.remove("bl_manip.txt")
        for n in bl: 
            m = [int(i) for i in n.split() if i.isdigit()]
            with open("bl_manip.txt", "a") as bl_manip:
                if not any(x in m for x in ls_NrAtoms):
                    print(m[0], m[1], file = bl_manip)
    os.remove("bl.txt")

    if bl_state == True: 
        __origpath__ = os.path.dirname(os.getcwd())
        os.chdir(__origpath__)

    # ba
    if ba_state == True: 
        __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
        os.chdir(__dirpath__)

    if os.path.exists("ba.txt"):
        with open("ba.txt") as ba: 
            ba.seek(0)
            ba = ba.readlines()
            if os.path.exists("ba_manip.txt"):
                os.remove("ba_manip.txt")
            for n in ba: 
                m = [int(i) for i in n.split() if i.isdigit()]
                with open("ba_manip.txt", "a") as ba_manip:
                    if not any(x in m for x in ls_NrAtoms):
                        print(m[0], m[1], m[2], file = ba_manip)
        os.remove("ba.txt")
        if os.stat("ba_manip.txt").st_size == 0: # Check if any bond angles are left, delete manip-file if empty
            os.remove("ba_manip.txt")
    
    if ba_state == True: 
        __origpath__ = os.path.dirname(os.getcwd())
        os.chdir(__origpath__)
    
    # da
    if da_state == True: 
        __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
        os.chdir(__dirpath__)

    if os.path.exists("da.txt"):
        with open("da.txt") as da: 
            da.seek(0)
            da = da.readlines()
            if os.path.exists("da_manip.txt"):
                os.remove("da_manip.txt")
            for n in da: 
                m = [int(i) for i in n.split() if i.isdigit()]
                with open("da_manip.txt", "a") as da_manip:
                    if not any(x in m for x in ls_NrAtoms):
                        print(m[0], m[1], m[2], m[3], file = da_manip)
        os.remove("da.txt")
        if os.stat("da_manip.txt").st_size == 0: # Check if any dihedral angles are left, delete manip-file if empty
            os.remove("da_manip.txt")

    if da_state == True: 
        __origpath__ = os.path.dirname(os.getcwd())
        os.chdir(__origpath__)       
        
    # H_Cart
    if os.path.exists("H_Cart_temp.txt"):
        os.remove("H_Cart_temp.txt")
    if os.path.exists("H_Cart_manip.txt"):
        os.remove("H_Cart_manip.txt")

    #### delete rows of H_Cart #####
    with open("H_Cart.txt") as H_Cart: 
        lines = H_Cart.readlines()
        H_Cart.close()

    ls_NrAtoms.sort(reverse = True)

    for x in ls_NrAtoms:
        del lines[3*(int(x)-1)]
        del lines[3*(int(x)-1)]
        del lines[3*(int(x)-1)]

    with open("H_Cart_temp.txt", "a") as H_Cart_temp:
        for line in lines: 
            H_Cart_temp.write(line)
        
    ##### delete columns of H_Cart ####
    with open("H_Cart_temp.txt", "r") as H_Cart_temp:
        lines = H_Cart_temp.readlines()
        
        line = 0
        for y in lines: 
            for x in ls_NrAtoms:
                y = y.split(" ")
                del y[3*(int(x)-1)]
                del y[3*(int(x)-1)]
                del y[3*(int(x)-1)]
                y = ' '.join(y)
                y = y.rstrip()    
            print(y, file = open("H_Cart_manip.txt", "a"))
            line = line + 1

    # if os.path.exists("H_Cart.txt"):
    #     os.remove("H_Cart.txt")
    if os.path.exists("H_Cart_temp.txt"):
        os.remove("H_Cart_temp.txt")


##############################################################################
###      Read manip-files; needed for b_mat.py and in delta_q.py           ###
##############################################################################

# read in the files, for later use

if os.path.exists("x0_manip.txt"):
    with open("x0_manip.txt", "r") as x0: # extract cartesian coordinates into list -> np.array
        x0_coords = read_xyz(x0)

elif os.path.exists("x0.txt"):
    with open("x0.txt", "r") as x0: 
        x0_coords = read_xyz(x0)
x0.close()

if os.path.exists("xF_manip.txt"):
    with open("xF_manip.txt", "r") as xF:
        xF_coords = read_xyz(xF)

elif os.path.exists("xF.txt"):
    with open("xF.txt", "r") as xF:
        xF_coords = read_xyz(xF)
xF.close()

# Generate the displacement-vector in Cartesian coordinates
delta_x = np.array(xF_coords) - np.array(x0_coords)
delta_x_list = delta_x.flatten().tolist()

##############################################################################
### Read primitives and return list; needed for b_mat.py and in delta_q.py ###
##############################################################################

# Read the connectivities of the atoms in the RIMs
# and caluculate the RIMs (= number of rows in the B-Matrix)
# Also generate an array that stores the RIM type information 
RIM_type = []

### Bond lengths ###
# check if atoms were deleted from bl.txt
if bl_state == True:
    __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
    os.chdir(__dirpath__)
if os.path.exists("bl_manip.txt"):
    bl_file = 'bl_manip.txt'
elif os.path.exists("bl.txt"):
    bl_file = 'bl.txt'
else:
    bl_file = 'None'
if os.path.exists(bl_file):
    bl = np.loadtxt(bl_file)
    if len(bl) == 0:
        {}
    elif bl.ndim == 1:
        Nbl = bl.ndim
        RIM_type.append("BL " + str(int(bl[0])) + " " + str(int(bl[1])) + " ")
        bl = [bl]
    else:
        Nbl = bl.shape[0]
        for i in range(Nbl):
            RIM_type.append("BL " + str(int(bl[i, 0])) + " " + str(int(bl[i, 1])) + " ")
if bl_state == True:
    __origpath__ = os.path.dirname(os.getcwd())
    os.chdir(__origpath__)

#### Bond angles ###
if ba_state == True:
    __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
    os.chdir(__dirpath__)
if os.path.exists("ba_manip.txt"):
    ba_file = 'ba_manip.txt'
elif os.path.exists("ba.txt"):
    ba_file = 'ba.txt'
else:
    ba_file = 'None'
if os.path.exists(ba_file):
    ba = np.loadtxt(ba_file)
    if len(ba) == 0:
        {}
    elif ba.ndim == 1:
        Nba = ba.ndim
        RIM_type.append("BA " + str(int(ba[0])) + " " + str(int(ba[1])) + " " + str(int(ba[2])) + " ")
        ba = [ba]
    else:
        Nba = ba.shape[0]
        for i in range(Nba):
            RIM_type.append("BA " + str(int(ba[i, 0])) + " " + str(int(ba[i, 1])) + " " + str(int(ba[i, 2])) + " ")
if ba_state == True:
    __origpath__ = os.path.dirname(os.getcwd())
    os.chdir(__origpath__)

# Dihedral angles
if da_state == True:
    __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
    os.chdir(__dirpath__)
if os.path.exists("da_manip.txt"):
    da_file = 'da_manip.txt'
elif os.path.exists("da.txt"):
    da_file = 'da.txt'
else:
    da_file = 'None'
if os.path.exists(da_file):
    da = np.loadtxt(da_file)
    if len(da) == 0:
        {}
    elif da.ndim == 1:
        Nda = da.ndim
        RIM_type.append("DA " + str(int(da[0])) + " " + str(int(da[1])) + " " + str(int(da[2])) + " " + str(int(da[3])) + " ")
        da = [da]
    else:
        Nda = da.shape[0]
        for i in range(Nda):
            RIM_type.append("DA " + str(int(da[i, 0])) + " " + str(int(da[i, 1])) + " " + str(int(da[i, 2])) + " " + str(int(da[i, 3])) + " ")

if da_state == True:
    __origpath__ = os.path.dirname(os.getcwd())
    os.chdir(__origpath__)

