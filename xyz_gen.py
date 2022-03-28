
import sys
import os
from jedi_functions import search_lines

"""

Script to extract the geometry of a molecule and save it as xyz file. 

implemented programs:
Q-Chem or ORCA

possible files: 
Single Point Calculation or Geometry Optimization

use as "python xyz_gen.py <input_file.out> <program> <geometry>"

<program> : Q_Chem or ORCA
<geometry> : x0 or xF

"""

in_file = sys.argv[1]
program = sys.argv[2]
geom = sys.argv[3]

if geom == "x0": 
    if os.path.exists("x0.txt"):
        os.remove("x0.txt")
    out_file = open("x0.txt", "a")
elif geom == "xF": 
    if os.path.exists("xF.txt"):
        os.remove("xF.txt")
    out_file = open("xF.txt", "a")

if program == "Q_Chem":
    with open(in_file) as in_file: # open single point of strained molecule
        in_file.seek(0)
        in_file = in_file.readlines()

        # number of atoms
        atoms_line = search_lines("$molecule", in_file)
        atom_count = 0
        for line in range(atoms_line+1, len(in_file)):
            if in_file[line].startswith("$end"):
                break
            atom_count +=1
        print(int(atom_count), "\n", file = out_file)

        # cartesian coordinates
        cart_line = search_lines("Standard Nuclear Orientation (Angstroms)", in_file)    #search for string to determine start of printout of coordinates
        for i in range(cart_line+2,cart_line+2+int(atom_count)): 
            cart = in_file[i].split()
            print(float(cart[2])*1.889725989, '\t', float(cart[3])*1.889725989, '\t', float(cart[4])*1.889725989, file = out_file)

elif program == "ORCA": 
    with open(in_file) as in_file:
        in_file.seek(0)
        in_file = in_file.readlines()
        cart_line = search_lines("CARTESIAN COORDINATES (A.U.)", in_file) 

        # number of atoms
        atom_count = 0
        for line in range(cart_line+1, len(in_file)):
            if in_file[line].startswith("----------------------------"):
                atom_count = atom_count - 1
                break
            atom_count +=1
        print(atom_count, "\n", file = out_file)

        # cartesian coordinates
        for j in range(cart_line+2, cart_line+2+int(atom_count)): 
            cart = in_file[j].split()
            print(float(cart[5]), '\t', float(cart[6]),'\t', float(cart[7]), file = out_file)

out_file.close()