# Main routine of the JEDI analysis. 

import numpy as np
import os
import argparse
import random  # needed for quotes 

# Initializing variables for optional arguments
directory_flag = False  # Only if the user specifies the name of a directory, this is set to true
vmd_flag = True  # Generate tcl scripts for generating color-coded structures in VMD by default
man_strain = None  # Set an optional maximum strain for VMD to None by default
modus = None

# Check if any optional positional arguments are given
parser = argparse.ArgumentParser()
parser.add_argument('--d', help = "Please specify a directory after the --d flag.")
parser.add_argument('--v', nargs = '+', help = "Either specify a maximum strain and a modus or call with 'n' if you wish no vmd analysis.")
args = parser.parse_args()

# turn flags to variables and set to True or False
if args.d: 
    directory_flag = True
    directory = args.d 
else: 
    directory = None

if args.v: 
    if args.v == ['n']:
        vmd_flag = False
    else:
        man_strain = args.v[0]
        modus = args.v[1]

if __name__ == '__main__': 

    print("\n Preparing the JEDI analysis...", "\n")
    
    from jedi_files import energies_file # import energies_file marker (True if E_geoms.txt exists)

    from jedi_directory import *

    import jedi_rims

    # run kill_atoms.py, to generate a list of which atoms should be ignored in JEDI; continuing jedi.py if no atoms should be deleted. 
    from jedi_kill_atoms import RIM_type
    # import list of atoms, that should be ignored in JEDI-Analysis and updated x0, xF

    # run b_mat.py, to calculate the B-Matrix.
    import jedi_b

    # run delta_q.py and calculate q0, qF and delta_q
    from jedi_delta_q import delta_q


    ##### Read in multiple files generated from imported scripts: #####
    # Transposed B-Matrix from b_mat.txt (generated from b_mat.py)
    # Hessian in cartesian coordinates from H_Cart.txt or H_Cart_manip.txt (in case atoms are deleted in kill_atoms.txt) (generated from hessian.py)

    # Read the B-Matrix
    B = np.loadtxt('b_mat.txt')
    B_transp = np.transpose(B)

    if os.path.exists("H_Cart_manip.txt"):
        with open("H_Cart_manip.txt", "r") as H_Cart_file:
            H_cart = np.loadtxt('H_Cart_manip.txt')
    elif os.path.exists("H_Cart.txt"):
        with open("H_Cart.txt", "r") as H_Cart_file:
            H_cart = np.loadtxt('H_Cart.txt')
    H_Cart_file.close()
    
    if energies_file == True:
        with open('E_geoms.txt', 'r') as energies_file: 
            all_E_geometries = np.loadtxt(energies_file)
            E_geometries = all_E_geometries[0]
        energies_file.close()

    ###########################
    ##  Matrix Calculations  ##
    ###########################

    # Calculate the number of RIMs (= number of rows in the B-Matrix), equivalent to number of redundant internal coordinates
    NRIMs = int(len(RIM_type))

    # Calculate the pseudoinverse of the B-Matrix and its transposed (take care of diatomic molecules specifically)
    if B.ndim == 1:
        B_plus = B_transp/2
        B_transp_plus = B/2
    else:
        B_plus = np.linalg.pinv(B, 0.0001)
        B_transp_plus = np.linalg.pinv( np.transpose(B),0.0001 )


    # Calculate the P-Matrix (eq. 4 in Helgaker's paper)
    P = np.dot(B, B_plus)


    #############################################
    #	    	   JEDI analysis	        	#
    #############################################

    # Calculate the Hessian in RIMs (take care to get the correct multiplication for a diatomic molecule
    if B.ndim == 1:
        H_q = B_transp_plus.dot( H_cart ).dot( B_plus )
    else:
        H_q = P.dot( B_transp_plus ).dot( H_cart ).dot( B_plus ).dot( P )

    # Calculate the total energies in RIMs and its deviation from E_geometries
    E_RIMs_total = 0.5 * np.transpose( delta_q ).dot( H_q ).dot( delta_q )

    proc_geom_RIMs = 100 * ( E_RIMs_total - E_geometries ) / E_geometries

    # Get the energy stored in every RIM (take care to get the right multiplication for a diatomic molecule)
    E_RIMs = []
    if B.ndim == 1:
        E_current = 0.5 * delta_q[0] * H_q * delta_q[0]
        E_RIMs.append(E_current)
    else:
        for i in range(NRIMs):
            E_current = 0
            for j in range(NRIMs):
                E_current += 0.5 * delta_q[i] * H_q[i,j] * delta_q[j]
            E_RIMs.append(E_current)

    # Get the percentage of the energy stored in every RIM
    proc_E_RIMs = []
    for i in range(NRIMs):
        proc_E_RIMs.append( 100 * E_RIMs[i] / E_RIMs_total )



    #############################################
    #	    	   Output section	        	#
    #############################################

    # Header
    print("\n \n")
    print(" ************************************************")
    print(" *                 JEDI ANALYSIS                *")
    print(" *       Judgement of Energy DIstribution       *")
    print(" ************************************************\n")

    # Comparison of total energies
    print("                   Strain Energy (h)  Deviation (%)")
    print("      Geometries      " + "%.8f" % E_geometries + "           -" )
    print('%5s%16.8f%14.2f' % (" Red. Int. Modes", E_RIMs_total, proc_geom_RIMs))


    # JEDI analysis
    print("\n RIM No.    RIM type             Percentage    Energy (h)")
    for i in range(NRIMs):
        print('%6i%7s%-18s%9.1f%17.7f' % (i+1, " ", RIM_type[i], proc_E_RIMs[i], E_RIMs[i]))

    # Write the energies to a file
    f = open('energies.txt', 'w')
    f.write('{} {}\n'.format(E_geometries, E_RIMs_total))
    f.close()

    # Write the parts of the energy stored in the RIMs to a file
    f = open('E_RIMs.txt', 'w')
    for i in E_RIMs:
        f.write("%s\n" % i)
    f.close()

    # Write the percentages of the energy stored in the RIMs to a file
    f = open('E_RIMs_perc.txt', 'w')
    for i in proc_E_RIMs:
        f.write("%s\n" % i)
    f.close()

    if vmd_flag == True: 
        pass

        import vmd_gen

    # Fairwell messages
    print("\n")
    print("\nJEDI terminated successfully.\n")
    quotes = open('jedi_quotes-library.txt').read().splitlines()
    quote = random.choice(quotes)
    print(quote)
    
    print("\n")