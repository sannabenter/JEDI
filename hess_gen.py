import warnings
import sys
import os
import glob
import numpy as np
from jedi_functions import search_lines

"""

Script to extract the Hessian in cartesian coordinates; prints the Hessian to H_cart.txt. 

implemented programs:
Q-Chem or ORCA

possible files: 
Frequency Calculation

use as "python hess_gen.py <input_file.out> <program> <NAtoms>

<program> : Q_Chem or ORCA
<NAtoms>  : Number of Atoms

"""

if os.path.exists("H_Cart_manip.txt"):
    os.remove("H_Cart_manip.txt")

vib_file = sys.argv[1]
program = sys.argv[2]
NAtoms = sys.argv[3]

NCarts = 3*int(NAtoms)

warnings.simplefilter(action='ignore', category=FutureWarning) #to avoid error message induced by checking if all entries in H_Cart == zero 
# Error due to combination of python command and numpy.

# Initialization of various variables and arrays
add_block = False #default False for first block of coordinates, set to True during script when additional block of coordinates begins
Stack = False #default False for first block, set to True when second block of coordinates begin #personal note: combine add_block and stack as increment (?)
fur_H_Cart = np.zeros(6) #initializes vector of coordinates
Fur_H_Cart = np.zeros([int(NCarts), 6]) #initializes array of blocks of coordinates to stack onto H_Cart
H_Cart = np.zeros([int(NCarts), int(NCarts)]) #array of Hessian, FINAL PRINTOUT

### Q-Chem ###

if program == "Q_Chem": 
    
    with open(vib_file) as file: 
        file.seek(0)
        file = file.readlines()

        hess_line = search_lines("Hessian of the SCF Energy", file)

        for i in range(hess_line+1, len(file)): #starts reading at catchphrase of Hessian printout, passed w/ search_script function

            if file[i].startswith("         "):    # 12 spaces indicting row of atomnumbers: new block of coordinates for 6 atoms
                add_block = True    #see above, indicator for new block of coordinates
                if Stack == True:   #see above, if set to True, Stacking gained block of coordinates onto H_Cart
                    # print("if, Stacking horizontally now", H_Cart, Fur_H_Cart)
                    H_Cart = np.hstack((H_Cart, Fur_H_Cart)) #stacks two sets of coordinates together (gained in elif-statement)
                    Fur_H_Cart = np.zeros([int(NCarts), 6]) #resetting Fur_H_Cart and fur_H_Cart
                    fur_H_Cart = np.zeros(6)  
                    continue
                else:  
                    continue
        
            
            elif file[i].startswith("  "):       # 2 spaces indicting row of coordinates     
                temp = file[i].split()
                H_singlecart = ' '.join(temp[1:])

                if add_block == False:   #False for first line of first block of coordinates (atoms 1-6)
                                
                    if np.all(H_Cart == 0):              #checks if H_Cart is filled w/ zeros, meaning no input so far -> first line of coordinates
                        H_Cart = np.array(H_singlecart) #fills H_Cart with coordinates in first line
                    else: 
                        fur_H_Cart = np.array(H_singlecart) #stacks further coordinates onto first line
                        H_Cart = np.vstack((H_Cart, fur_H_Cart))
                        fur_H_Cart = np.zeros(6)

                else:                    #for further lines of coordinates in further blocks
                    if np.all(Fur_H_Cart == 0):  #see above, change to Fur_H_Cart, to then stack onto H_Cart in if-statement
                        Fur_H_Cart = np.array(H_singlecart)
                    else: 
                        fur_H_Cart = np.array(H_singlecart)
                        Fur_H_Cart = np.vstack((Fur_H_Cart, fur_H_Cart))
                        Stack = True


            elif file[i] == "\n" or file[i].startswith(" ---") : # empty line or line filled with '-', indicating end of hessian printout
                # #last stacking of Coordinate-Blocks before breaking out of loop
                if H_Cart.shape[0] != Fur_H_Cart.shape[0]:
                    print("ERROR, can't stack the arrays, I need further inlook into shapes of the two arrays to stack.")
                    H_Cart = np.hstack((H_Cart, Fur_H_Cart[:-1])) 
                    break
                
                H_Cart = np.hstack((H_Cart, Fur_H_Cart))
                break

    with open("H_Cart.txt", "w+") as out_file:
        np.savetxt(out_file, H_Cart, fmt='% s')
        out_file.close()


### ORCA ###

if program == "ORCA": 
    for file in glob.glob( "*.hess" ):
        with open(file) as file:
            hess_line = search_lines("$hessian", file)
            file.seek(0)
            file = file.readlines()

            for i in range(hess_line+2, len(file)): #starts reading at catchphrase of Hessian printout, passed w/ search_script function

                if file[i].startswith("         "):    #12 spaces indicting row of atomnumbers: new block of coordinates for 6 atoms
                    add_block = True    #see above, indicator for new block of coordinates
                    if Stack == True:   #see above, if set to True, Stacking gained block of coordinates onto H_Cart
                    #print("if, Stacking horizontally now", H_Cart, Fur_H_Cart)
                        H_Cart = np.hstack((H_Cart, Fur_H_Cart)) #stacks two sets of coordinates together (gained in elif-statement)
                        Fur_H_Cart = np.zeros([int(NCarts), 6]) #resetting Fur_H_Cart and fur_H_Cart
                        fur_H_Cart = np.zeros(6)  
                        continue
                    else:  
                        continue
        
            
                elif file[i].startswith("  "):       #2 spaces indicting row of coordinates     
                    temp = file[i].split()
                    H_singlecart = ' '.join(temp[1:])

                    if add_block == False:   #False for first line of first block of coordinates (atoms 1-6)
                                
                        if np.all(H_Cart == 0):              #checks if H_Cart is filled w/ zeros, meaning no input so far -> first line of coordinates
                            H_Cart = np.array(H_singlecart) #fills H_Cart with coordinates in first line
                        else: 
                            fur_H_Cart = np.array(H_singlecart) #stacks further coordinates onto first line
                            H_Cart = np.vstack((H_Cart, fur_H_Cart))
                            fur_H_Cart = np.zeros(6)

                    else:                    #for further lines of coordinates in further blocks
                        if np.all(Fur_H_Cart == 0):  #see above, change to Fur_H_Cart, to then stack onto H_Cart in if-statement
                            Fur_H_Cart = np.array(H_singlecart)
                        else: 
                            fur_H_Cart = np.array(H_singlecart)
                            Fur_H_Cart = np.vstack((Fur_H_Cart, fur_H_Cart))
                            Stack = True


                elif file[i] == "\n": #regular expression for text, indicating end of hessian printout
                    # #last stacking of Coordinate-Blocks before breaking out of loop
                    if H_Cart.shape[0] != Fur_H_Cart.shape[0]:
                        print("ERROR, can't stack the arrays, you need further inlook into shapes of the two arrays to stack.")
                        H_Cart = np.hstack((H_Cart, Fur_H_Cart[:-1])) 
                        break
                
                    H_Cart = np.hstack((H_Cart, Fur_H_Cart))
                    break

        with open("H_Cart.txt", "w+") as out_file:
            np.savetxt(out_file, H_Cart, fmt='% s')
            out_file.close()


# Final check if everything is okay
# Checking if file exists
if os.path.exists("H_Cart.txt"):
    pass
else: 
    print("ERROR, something wrong with hessian.py, could not find H_Cart.txt.")

#H_Cart.txt is a readable file with the dimension: NCarts x NCarts   
H_Cart = np.genfromtxt("H_Cart.txt")
if H_Cart.shape[0] != int(NCarts):
    print("ERROR, number of rows in H_Cart.txt is not correct. Please check the Output.")
if H_Cart.shape[1] != int(NCarts):
    print("ERROR, number of columns in H_Cart.txt is not correct. Please check the Output.")
