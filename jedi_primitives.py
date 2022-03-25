# This script is called by jedi.py.
# It knows opt, the Q-Chem output file of the geometry optimization.
# Out of this file, it gets the primitive internal modes of the molecule and writes them to bl.txt, ba.txt and da.txt.
# ba.txt and da.txt are only produced if the molecule has bond angles and dihedrals.
# It is crucial that the print level of the relaxed geometry optimization, geom_opt_print, is at least 7 when donig Q-Chem Calculations.
import re
import os
import numpy as np
import jedi_files
from jedi_functions import search_lines, search_line
from jedi_directory import ba_state, bl_state, da_state
from jedi import directory

if bl_state == False: 
    # Checking if bl.txt, ba.txt and da.txt already exist. Deleting them, if they do.
    if os.path.exists("bl.txt"):
        os.remove("bl.txt")
    if os.path.exists("bl_manip.txt"):
        os.remove("bl_manip.txt")

if ba_state == False: 
    if os.path.exists("ba.txt"):
        os.remove("ba.txt")
    if os.path.exists("ba_manip.txt"):
        os.remove("ba_manip.txt")

if da_state == False:
    if os.path.exists("da.txt"):
        os.remove("da.txt")
    if os.path.exists("da_manip.txt"):
        os.remove("da_manip.txt")
    


if ba_state or bl_state or da_state == False:

    if jedi_files.Q_Chem == True:
        with open(jedi_files.opt_file) as opt:    
            opt.seek(0)
            opt = opt.readlines()

        if da_state == False: 
            # checking if there are torsions in molecule, if so: print them to da.txt. If not, proceed with bending.
            if search_line("There are      0 Torsions", opt) != 0:
                print("\tINFO: There are no torsions in your molecule, so I'm not writing da.txt.")
            else: 
                torsions = search_lines("Primitive Torsions:", opt)
                for i in range(torsions, len(opt)):
                    if re.search("^[0-9 ]+$", opt[i]):  
                        print(opt[i], end = '', file = open("da.txt", "a"))
                    else: 
                        break

        if ba_state == False: 
            # checking if there are bendings in molecule, if so: print them to ba.txt. If not, proceed with stretches.
            if search_line("There are      0 Bends", opt) != 0:
                print("\tINFO: There are no bendings in your molecule, so I'm not writing ba.txt.")
            else: 
                bends = search_lines("Primitive Bends:", opt)
                for j in range(bends, len(opt)):
                    if re.search("^[0-9 ]+$", opt[j]):  
                        print(opt[j], end = '', file = open("ba.txt", "a"))
                    else: 
                        break

        if bl_state == False: 
            # searching for stretches and printing them to bl.txt
            stretches = search_line("Primitive Stretches:", opt)
            for k in range(stretches, len(opt)):
                if re.search("^[0-9 ]+$", opt[k]):  
                    print(opt[k], end = '', file = open("bl.txt", "a"))
                else: 
                    break

    if jedi_files.ORCA == True: 
        with open(jedi_files.opt_file) as opt:   
            opt.seek(0)
            opt = opt.readlines()
            coords = search_lines("Redundant Internal Coordinates", opt)

            for l in range(coords+6, len(opt)):
                if opt[l].startswith("    ---"):
                    break
                else:
                    if bl_state == False: 
                        if (re.search("A|B|D", opt[l])).group() == 'B': 
                            primitives = re.split("[(),]|\s{3}", opt[l])
                            print(int(primitives[3])+1, int(primitives[5])+1, file = open("bl.txt", "a"))

                    if ba_state == False:
                        if (re.search("A|B|D", opt[l])).group() == 'A': 
                            primitives = re.split("[(),]|\s{3}", opt[l])
                            print(int(primitives[3])+1, int(primitives[5])+1, int(primitives[7])+1, file = open("ba.txt", "a"))
                    
                    if da_state == False: 
                        if (re.search("A|B|D", opt[l])).group() == 'D': 
                            primitives = re.split("[(),]|\s{3}", opt[l])
                            print(int(primitives[3])+1, int(primitives[5])+1, int(primitives[7])+1, int(primitives[9])+1, file = open("da.txt", "a"))


              