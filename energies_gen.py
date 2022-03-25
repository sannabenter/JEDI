import sys
import os
from jedi_functions import search_lines

"""

Script to extract the geometry of a molecule and save it as xyz file. 

implemented programs:
Q-Chem or ORCA

possible input files: 
Single Point Calculation or Geometry Optimization

use as "python energies_gen.py <opt_file> <force_opt_file> <program> "

"""

opt_file = sys.argv[1]
force_opt_file = sys.argv[2]
program = sys.argv[3]


if program == "Q_Chem":

    with open(opt_file) as opt:
        opt.seek(0)
        opt = opt.readlines()
        j = search_lines("Final energy is", opt)
        E_0 = opt[j-1].split()
        E_0 = float(E_0[3])

    with open(force_opt_file) as force_opt:
        force_opt.seek(0)
        force_opt = force_opt.readlines()
        j = search_lines("Total energy in the final basis set", force_opt)
        E_F = force_opt[j-1].split()
        E_F = float(E_F[8])

if program == "ORCA":

    with open(opt_file) as opt:
        opt.seek(0)
        opt = opt.readlines()
        j = search_lines("FINAL SINGLE POINT ENERGY", opt)
        E_0 = opt[j-1].split()
        E_0 = float(E_0[4])

    with open(force_opt_file) as force_opt:
        force_opt.seek(0)
        force_opt = force_opt.readlines()
        j = search_lines("FINAL SINGLE POINT ENERGY", force_opt)
        E_F = force_opt[j-1].split()
        E_F = float(E_F[4])

if os.path.exists("E_geoms.txt"):
    print("Found file \"E_geoms\" while running energies_gen.py; deleting file to write new one.")
    os.remove("E_geoms.txt")


E_geometries = E_F - E_0

f = open('E_geoms.txt', 'w')
f.write(f'{E_geometries} \t {E_F} \t {E_0}')
f.close()