import os
import sys

"""

This script is called by jedi.py

It checks if the needed input data is there (x0.txt, xF.txt and H_Cart.txt). 
The script also checks if the optional files with energies are given. 

"""

# Check if all the files are in the directory.

if not os.path.exists("x0.txt"):
    print("\t \t No file containing the relaxed geometry found.")
    print("\t \t Please create file containing the geometry called 'x0.txt'.")
    sys.exit()

if not os.path.exists("xF.txt"):
    print("\t \t No file containing the deformed geometry found.")
    print("\t \t Please create file containing the geometry called 'xF.txt'.")
    sys.exit()

if not os.path.exists("H_Cart.txt"):
    print("\t \t No file containing the hessian in cartesian coordinates.")
    print("\t \t Please create file containing the hessian called 'H_Cart.txt'.")
    sys.exit()

# Get the atomnumber and compare xF and x0. 

with open("x0.txt", encoding="utf8", errors='ignore') as x0:
    x0_coords = (x0.read())
    NAtom_x0 = x0_coords.split('\n', 1)[0]
    x0.close()
with open("xF.txt", encoding="utf8", errors='ignore') as xF:
    xF_coords = (xF.read())
    NAtom_xF = xF_coords.split('\n', 1)[0]
    xF.close()

if NAtom_x0 == NAtom_xF: 
    NAtoms = int(NAtom_x0)
    NCarts = 3*NAtoms
elif NAtom_x0 != NAtom_xF: 
    print("\t \t xF.txt and x0.txt do not show the same atomnumber.")
    print("\t \t Please check the files.")

# Check if the optional energy file is in the directory. 
energies_file = False
if os.path.exists("E_geoms.txt"):
    energies_file = True