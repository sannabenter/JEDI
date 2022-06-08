import os
from collections import Counter
import numpy as np
import pandas as pd
from jedi_directory import directory, bl_state, ba_state, da_state

"""

This script is called by jedi.py

It converts cartesian coordinates (from x0.txt) into redundant internal modes. 
The script creates three files: 

bl.txt - containing all the bonds
ba.txt - containing all the bondangles
da.txt - containing all the torsionangles

"""

print("Starting jedi_rims.py to calculate redundant internal modes from cartesian coordinates.")

if os.path.exists("bl.txt"):
    os.remove("bl.txt")
if os.path.exists("ba.txt"):
    os.remove("ba.txt")
if os.path.exists("da.txt"):
    os.remove("da.txt")

df_lib_elements = pd.DataFrame(columns=('radius', 'element')) 

row = 0
with open("jedi_elements-library.txt", "r") as lib_elements: 
    for element_line in lib_elements: 
        element_line = element_line.split()
        
        df_lib_elements.loc[row] = [element_line[0], element_line[2]]
        row += 1

def vector_length(x_atom1, y_atom1, z_atom1, x_atom2, y_atom2, z_atom2): # function to calculate bondlength
    vec = [0, 0, 0]
    vec[0] = float(x_atom2) - float(x_atom1)
    vec[1] = float(y_atom2) - float(y_atom1)
    vec[2] = float(z_atom2) - float(z_atom1)

    len_vec = np.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)

    return len_vec


df_bl = pd.DataFrame(columns=('BL_1', 'BL_2')) # dataframe containing bondlengths
df_ba = pd.DataFrame(columns=('BA_1', 'BA_2', 'BA_3')) # dataframe containing bondangles
df_torsionable_bonds = pd.DataFrame(columns=('TA_Atom_1', 'TA_Atom_2')) # dataframe containing all bonds with torsion angles
df_da = pd.DataFrame(columns=('DA_1', 'DA_2', 'DA_3', 'DA_4')) # dataframe containing torsionangles


with open("x0.txt", "r") as x0: # extract cartesian coordinates into list -> dataframe
    ln = 0
    elements = []
    x_coords = []
    y_coords = []
    z_coords = []
    for line in x0: 
        if ln > 1:
            coords = line.strip("\t").split()
            elements.append(coords[0])
            x_coords.append(coords[1])
            y_coords.append(coords[2])
            z_coords.append(coords[3])
        ln += 1

df_coords = pd.DataFrame(
    {'x': x_coords,
     'y': y_coords,
     'z': z_coords
    })

    ####################################
    ############ BOND LENGTHS ##########
    ####################################

if bl_state == False: 

    # create dataframe containing all bonds (df_bl)
    row_index = 0 # indexes row of dataframe for each bond
    for self_index in range(0, len(x_coords)): # iterates through all atom indices
        for other_index in range(0, len(x_coords)): # iterates through all atom indices
            if other_index > self_index: # only iterate through every bond once

                self_element = elements[self_index]
                x = df_coords.at[int(self_index), 'x']
                y = df_coords.at[int(self_index), 'y']
                z = df_coords.at[int(self_index), 'z']

                other_element = elements[other_index]
                x_other = df_coords.at[int(other_index), 'x']
                y_other = df_coords.at[int(other_index), 'y']
                z_other = df_coords.at[int(other_index), 'z']

                len_vec = vector_length(x, y, z, x_other, y_other, z_other) # calculate vector length

                self_loc = df_lib_elements[df_lib_elements['element']==self_element].index.values
                other_loc = df_lib_elements[df_lib_elements['element']==other_element].index.values

                self_radius = df_lib_elements['radius'].iloc[self_loc]
                other_radius = df_lib_elements['radius'].iloc[other_loc]

                virtual_bl = (float(self_radius) + float(other_radius))*1.889725989

                if abs(len_vec-virtual_bl) < 0.3: 
                    df_bl.loc[row_index] = [other_index+1, self_index+1] # add bondlengths to dataframe

                    row_index += 1 
    
    if not df_bl.empty: 
        with open("bl.txt", "a") as bl_file:
            for index, row in df_bl.iterrows():
                print(row['BL_1'],"\t", row['BL_2'], file = bl_file) # create file containing bonds
            bl_file.close()


    ####################################
    ############ BOND ANGLES ###########
    ####################################

if ba_state == False: 
    row_index = 0
    #create dataframe containing all angles (df_ba)
    for self_index, self_row in df_bl.iterrows(): # iterates through rows of bonds
        for other_index, other_row in df_bl.iterrows(): # iterates through rows of bonds
            if other_index > self_index: 
                temp_ba_list = [self_row['BL_1'], self_row['BL_2'], other_row['BL_1'], other_row['BL_2']]

                temp_ba_counter = Counter(temp_ba_list) # counts all entries in temporary bondangle list, counts duplicates

                connecting_atom = list([item for item in temp_ba_counter if temp_ba_counter[item]>1]) # checks which atom is duplicate

                other_atoms = [] # list collecting other atoms than connecting atom 
                if connecting_atom: # duplicate atom is connecting atom
                    for atom in temp_ba_list: 
                        if atom not in connecting_atom: 
                            other_atoms.append(atom)
                    
                    df_ba.loc[row_index] = [other_atoms[0], connecting_atom[0], other_atoms[1]] # add bondlengths to dataframe
                    row_index += 1 

    # sort the dataframe according to Bakken and Helgaker (used to calculate b-matrix in jedi_b.py)
    df_ba_sorted = df_ba.sort_values(by=['BA_2', 'BA_3'])

    if not df_ba.empty: 
        with open("ba.txt", "a") as ba_file:
            for index, row in df_ba.iterrows():
                print(row['BA_1'], "\t", row['BA_2'], "\t", row['BA_3'], file = ba_file) # create file containing bond angles
            ba_file.close()


    ####################################
    ########### TORSION ANGLES #########
    ####################################


if da_state == False: 
    row_index = 0
    torsionable_bonds = []
    #create dataframe containing list of all bonds with torsion angles (df_torsionable_bonds)
    for self_index, self_row in df_bl.iterrows(): # iterates through rows of bonds
        bond_partner1 = False # if both bond partners are set to True, no terminal bond. Thus, possible torsion around bond.
        bond_partner2 = False
        for other_index, other_row in df_bl.iterrows(): # iterates through rows of bonds
            if other_index != self_index: # only iterate bonds other than self
                if other_row['BL_1'] == self_row['BL_1'] or other_row['BL_2'] == self_row['BL_1']: # Check first Atom
                    bond_partner1 = True # Set to True if neighbouring atom
                    
                if other_row['BL_1'] == self_row['BL_2'] or other_row['BL_2'] == self_row['BL_2']: # Check second Atom#
                    bond_partner2 = True # Set to True if neighbouring atom

                if bond_partner1 == True and bond_partner2 == True: # if both bond partners are set to True, no terminal bond. Thus, possible torsion around bond.
                    df_torsionable_bonds.loc[row_index] = [self_row['BL_1'], self_row['BL_2']] 
                    bond_partner1 = False
                    bond_partner2 = False
                        
                    row_index += 1 

    row = 0
    for torsionable_index, torsionable_row in df_torsionable_bonds.iterrows():
        TA_Atoms_0 = [] 
        TA_Atoms_3 = [] 
        TA_Atom_0 = False # atom connected to TA_Atom_1
        TA_Atom_3 = False # atom connected to TA_Atom_2
        for other_index, other_row in df_bl.iterrows(): # iterates through rows of bonds
            if other_row['BL_1'] == torsionable_row['TA_Atom_1'] and other_row['BL_2'] == torsionable_row['TA_Atom_2']: 
                continue

            ### FIRST ATOM CONNECTION
            elif other_row['BL_1'] == torsionable_row['TA_Atom_1'] or other_row['BL_2'] == torsionable_row['TA_Atom_1']:     

                if other_row['BL_1'] == torsionable_row['TA_Atom_1']:
                    TA_Atom_0 = other_row['BL_2']

                else: 
                    TA_Atom_0 = other_row['BL_1']
                TA_Atoms_0.append(TA_Atom_0)

            ### SECOND ATOM CONNECTION
            if other_row['BL_1'] == torsionable_row['TA_Atom_2'] or other_row['BL_2'] == torsionable_row['TA_Atom_2']:
                if other_row['BL_1'] == torsionable_row['TA_Atom_2']:
                    TA_Atom_3 = other_row['BL_2']

                else: 
                    TA_Atom_3 = other_row['BL_1']
                TA_Atoms_3.append(TA_Atom_3)
                
        for single_TA_Atom_1 in TA_Atoms_0: 
            for single_TA_Atom_3 in TA_Atoms_3: 
                df_da.loc[row] = [single_TA_Atom_1,  torsionable_row['TA_Atom_1'], torsionable_row['TA_Atom_2'], single_TA_Atom_3]
                row += 1

    if not df_da.empty: 
        with open("da.txt", "a") as da_file:
            for index, row in df_da.iterrows():
                print(row['DA_1'], "\t", row['DA_2'], "\t", row['DA_3'], "\t", row['DA_4'], file = da_file) # create file containing torsion angles
            da_file.close()