import numpy as np
import os
import jedi_files
import jedi_functions # python script containing all functions needed for jedi.py
from jedi_kill_atoms import ls_NrAtoms, x0_coords, RIM_type

"""

This script is called by jedi.py

It calculates the B-Matrix according to [1].

[1] V. Bakken, T. Helgaker, J. Chem. Phys. 117 (20) 2002

"""

print("Starting b_mat.py to calculate the B-Matrix.")

if len(RIM_type) == 0:
    print("\t INFO: Something might be wrong with the list of deleted atoms in kill_atoms.txt, as it seems that there are no redundant internal coordinates left.")


# Get number of atoms from basic.py, subtract number of killed atoms
NAtoms = int(jedi_files.NAtoms) - len(ls_NrAtoms)
NCart_coords = 3*int(NAtoms)

#################################################
##  Program to calculate B-Matrix starts here  ##
#################################################

# Initilization of columns to specifiy position in B-Matrix
column = 0


# create an array of empty B-Matrix in the needed dimension:
# number of rows: number of redundant internal coordinates
# number of columns: number of cartesian coordinates)
b = np.zeros([int(NCart_coords), int(len(RIM_type))], dtype=float)

for q in RIM_type:  # for loop for all redunant internal coordinates
    row = 0  # Initilization of columns to specifiy position in B-Matrix
    if len(q) == 0:  # no redundant internal coordinates, prints user-info (see line 75)
        break

    ########  Section for stretches  #########
    if q.startswith("BL"):
        BL = []
        RIM = q.split(" ")
        BL = [int(RIM[1]), int(RIM[2])]  # create list of involved atoms
        q_i, q_j = BL

        # apply kill_atoms functions to assigned atomnr.
        if len(ls_NrAtoms) > 0:
            for killed_atom in ls_NrAtoms:
                q_i = jedi_functions.kill_atoms(killed_atom, q_i)
                q_j = jedi_functions.kill_atoms(killed_atom, q_j)
        BL = [q_i, q_j]

        m = np.array((x0_coords[(q_i-1), :]))
        n = np.array((x0_coords[(q_j-1), :]))
        u = jedi_functions.vector_tp(m, n)

        for NAtom in range(1, int(NAtoms)+1):  # for-loop of Number of Atoms (3N)
            for xyz in range(0, 3):  # for-loop of cartesian coordinates of each Atom (x, y and z)
                for q in BL:
                    if NAtom == q:  # derivative of redundnat internal coordinate w/ respect to cartesian coordinates is not equal zero
                                    # if redundant internal coordinate (q) contains the Atomnumber (NAtoms) of the cartesian coordinate (x0_coords) from which is derived from.

                        # if-/elif-statement for the right sign-factor (see [1])
                        if q == q_i:
                            b_i = jedi_functions.deriv_bondlength(u, xyz, -1)
                            b[row, column] = b_i  # change value of zero array at specified position to b_i
                        elif q == q_j:
                            b_i = jedi_functions.deriv_bondlength(u, xyz, +1)
                            b[row, column] = b_i  # change value of zero array at specified position to b_i
                row += 1
        column += 1

    ########  Section for Bond Angles  #########
    elif q.startswith("BA"):
        BA = []
        row = 0
        RIM = q.split(" ")
        center_atom = int(RIM[2])  # define center_atom (redundant step)
        BA = [int(RIM[1]), int(RIM[2]), int(RIM[3])]  # create list of involved atoms
        q_i, q_j, q_k = BA

        if len(ls_NrAtoms) > 0:
            for killed_atom in ls_NrAtoms:
                q_i = jedi_functions.kill_atoms(killed_atom, q_i)
                q_j = jedi_functions.kill_atoms(killed_atom, q_j)
                q_k = jedi_functions.kill_atoms(killed_atom, q_k)
        BA = [q_i, q_j, q_k]

        m = np.array((x0_coords[(q_i-1), :]))  # create list of cartesian coordinates
        o = np.array((x0_coords[(q_j-1), :]))  # list are assigned to n, o and m (according to [1])
        n = np.array((x0_coords[(q_k-1), :]))

        u = jedi_functions.vector_tp(m, o)
        v = jedi_functions.vector_tp(n, o)

        BA.sort()  # sort list of involved atoms (sorted list necessary for correct stacking of B-Matrix Elements)
        for NAtom in range(1, int(NAtoms)+1):  # for-loop of Number of Atoms (3N)
            for xyz in range(0, 3):  # for-loop of cartesian coordinates of each Atom (x, y and z)
                for q in BA:
                    if NAtom == q:  # derivative of redundnat internal coordinate w/ respect to cartesian coordinates is not equal zero
                                    # if redundant internal coordinate (q) contains the Atomnumber (NAtoms) of the cartesian coordinate (x0_coords) from which is derived from.
                        b_j = 0
                        if q == q_j:  # if-Statements for sign-factors
                            b_j = jedi_functions.deriv_bondangle(u, v, -1, -1, xyz)  # Q-Chem defines BA as m-o-n, where the atomnr. in the middle is the center-atom
                            b[row, column] = b_j                                # making it possible to define the center atom as RIM[2]
                        elif q == q_i:
                            b_j = jedi_functions.deriv_bondangle(u, v, 1, 0, xyz)
                            b[row, column] = b_j
                        elif q == q_k:
                            b_j = jedi_functions.deriv_bondangle(u, v, 0, 1, xyz)
                            b[row, column] = b_j
                row += 1
        column += 1

    ########  Section for Dihedral Angles  #########
    elif q.startswith("DA"):
        DA = []
        row = 0
        RIM = q.split(" ")
        DA = [int(RIM[1]), int(RIM[2]), int(RIM[3]), int(RIM[4])]  # create list of involved atoms
        q_i, q_j, q_k, q_l = DA

        if len(ls_NrAtoms) > 0:
            for killed_atom in ls_NrAtoms:
                q_i = jedi_functions.kill_atoms(killed_atom, q_i)
                q_j = jedi_functions.kill_atoms(killed_atom, q_j)
                q_k = jedi_functions.kill_atoms(killed_atom, q_k)
                q_l = jedi_functions.kill_atoms(killed_atom, q_l)
        DA = [q_i, q_j, q_k, q_l]

        m = np.array((x0_coords[(q_i-1), :]))  # create list of cartesian coordinates
        o = np.array((x0_coords[(q_j-1), :]))  # list are assigned to n, o, m and p (according to [1])
        p = np.array((x0_coords[(q_k-1), :]))
        n = np.array((x0_coords[(q_l-1), :]))

        u = jedi_functions.vector_tp(m, o)
        v = jedi_functions.vector_tp(n, p)
        w = jedi_functions.vector_tp(p, o)

        DA.sort()  # sort list of involved atoms (sorted list necessary for correct stacking of B-Matrix Elements)
        for NAtom in range(1, int(NAtoms)+1):  # for-loop of Number of Atoms (3N)
            for xyz in range(0, 3):  # for-loop of cartesian coordinates of each Atom (x, y and z)
                for q in DA:
                    if NAtom == q:  # derivative of redundant internal coordinate w/ respect to cartesian coordinates is not equal zero
                                    # if redundant internal coordinate (q) contains the Atomnumber (NAtoms) of the cartesian coordinate (x0_coords) from which is derived from.
                        b_k = 0
                        if q == q_i:  # if-Statements for sign-factors
                            b_k = jedi_functions.deriv_dihedralangle(u, v, w, 1, 0, 0, xyz)
                            b[row, column] = b_k
                        elif q == q_j:
                            b_k = jedi_functions.deriv_dihedralangle(u, v, w, -1, 0, 1, xyz)
                            b[row, column] = b_k
                        elif q == q_k:
                            b_k = jedi_functions.deriv_dihedralangle(u, v, w, 0, 1, -1, xyz)
                            b[row, column] = b_k
                        elif q == q_l:
                            b_k = jedi_functions.deriv_dihedralangle(u, v, w, 0, -1, 0, xyz)
                            b[row, column] = b_k

                row += 1
        column += 1

# Read the transposed B-Matrix and generate its transposed
B_transp = b

with open("b_transp.txt", "w+") as transp_file:
    np.savetxt(transp_file, B_transp, fmt='% f', delimiter='\t')
    transp_file.close()

B = np.transpose(B_transp)

with open("b_mat.txt", "w+") as out_file:
    np.savetxt(out_file, B, fmt='% f', delimiter='\t')
    out_file.close()


# Final check if everything is okay
# Checking if files exist
if os.path.exists("b_mat.txt"):
    pass
else: 
    print("ERROR, something wrong with b_mat.py, could not find b_mat.txt.")


#xF.txt and x0.txt are readables file with the dimension: NAtoms x 3   
B = np.genfromtxt("b_mat.txt")
if B.shape[0] != len(RIM_type):
    print("ERROR, number of rows in b_mat.txt does not equal number of cartesian coordinates. Please check b_mat.py.")
if B.ndim == 1:
    if B.ndim != int(NCart_coords):
        print("ERROR, number of columns in b_mat.txt does not equal number of redundant internal coordinates. Please check b_mat.py.")
else: 
    if B.shape[1] != int(NCart_coords):
        print("ERROR, number of columns in b_mat.txt does not equal number of redundant internal coordinates. Please check b_mat.py.")