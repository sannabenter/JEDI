#collection of functions used throughout JEDI-Calculation

import glob
import numpy as np
import os

############################################
####### functions to search (in) files #####
############################################

# Function to search string i in designated file, set hit = True, when string is in file
# used for finding out if Q-Chem or ORCA-Calculations were done
def search_file(i):
    for file in glob.glob( "*.out" ):
        with open(file) as file:
            for num, line in enumerate(file, 1):
                if i in line:
                    return True

# Function to search string in all out-files in current folder and return True if files are found
def find_files(search_string):
    file_hit = []
    for file in glob.glob( "*.out" ):
        with open(file) as file:
            if search_string in file.read():
                file_hit.append(file.name)
            file.close()
    if len(file_hit) == 1: 
        return True
    elif len(file_hit) != 1: 
        return False
            
# Function to search string in all out-files in current folder and return filename and line if string is found
def identify_files(search_string):
    file_hit = []
    line_hit = 0
    for file in glob.glob( "*.out" ):
        with open(file) as file:
            for num, line in enumerate(file, 1):
                if search_string in line:
                    file_hit = file.name
                    line_hit = num
                    return file_hit, line_hit

def check(it, num):
    it = iter(it)
    return all(any(it) for _ in range(num))

def file_error_message(filetype, string): 
    print(f"\t ERROR: Couldn't identify the {filetype} file while searching for {string}.")
    print(f"\t \t There is either more than one or no {filetype} file in the folder.")
    print(f"\t Checking jedi_manual_files.py for filenames.")

# Function to search string i in designated file and append lines of hit to list
# returns maximum of list of line numbers as line_hit
def search_lines(i, file):
    line_hit = []
    for num, line in enumerate(file, 1):
        if i in line:
            line_hit.append(num)
    return max(line_hit)

# Function to search string i in designated file and return line of hit 
def search_line(i, file):
    line_hit = 0
    for num, line in enumerate(file, 1):
        if i in line:
            line_hit = num
    return line_hit

# Function to search for a file in a directory given by path, sets variable to True for further handling. 
# Working directory needs to be changed to directory where to be found file is stored.
# Used in jedi_directory.py.
def dir_search_file(directory, file): 
    variable = False
    if os.path.isfile(file):
        print(f"\t Found file {file} in directory {directory}, using this file now.") 
        variable = True
        return variable
        
############################################
########### Functions xyz-files ############
############################################

def read_xyz(file): 
    
    ln = 0
    x_coords = []
    y_coords = []
    z_coords = []
    for line in file: 
        if ln > 1:
            coords = line.strip("\t").split()
            x_coords.append(float(coords[1]))
            y_coords.append(float(coords[2]))
            z_coords.append(float(coords[3]))
        ln += 1
        
    return np.array((x_coords, y_coords, z_coords)).T


############################################
########### B-Matrix Functions #############
############################################

# Function to adjust atomnumber in list of redundant internal coordinates, if atoms are "killed" in kill_atoms.txt
def kill_atoms(killed_atom, q):
    if q > killed_atom:
        q = q-1
        return int(q)
    else: 
        return int(q)

# Function to get the vector between two lists of Cartesian Coordinates
def vector_tp(m, n):
    return np.array([(m[0]-n[0]), (m[1]-n[1]), (m[2]-n[2])])

# Function to calculate the derivates of the bondlength between to atoms, where the positions are given in cartesian coordinates, 
# according to [1] (Citation see b_mat.py)
# Called by b_mat.py
def deriv_bondlength(u, xyz, i):
    nu = u / np.linalg.norm(u)
    b_i = -i * nu[xyz]
    return b_i

# Function to get the derivatives of angles formed by two vectors (u, v) in Cartesian coordinates, 
# i_amo and i_ano are the sign factors to the equation according to [1] (Citation see b_mat.py)
# Called by b_mat.py
def deriv_bondangle(u, v, i_amo, j_ano, xyz):
    d_ba = 0

    nu = u / np.linalg.norm(u) #normalize vectors
    nv = v / np.linalg.norm(v)
    angle = (np.arccos(np.dot(nu, nv)))/np.pi*180 # angle between v and u

    if angle == 180:
        if (np.arccos(np.dot(nu, (np.array([1, -1, 1])))/np.pi)*180) == 180:
            w = np.cross(nu, ([-1, 1, 1]))
        else: 
            w = np.cross(nu, ([1, -1, 1]))
    else:
        w = np.cross(nu, nv)
        
    nw = w / np.linalg.norm(w)

    d_ba = (i_amo * ((np.cross(nu, nw))[xyz]/np.linalg.norm(u))) + (j_ano * ((np.cross(nw, nv))[xyz]/np.linalg.norm(v))) # equation to calculate dBA/dx [1]

    return d_ba

# Function to get the derivatives of dihedral angles formed by three vectors (u, v, w) in Cartesian coordinates, 
# i_amo, i_apn and i_aop are the sign factors to the equation according to [1] (Citation see b_mat.py)
# Called by b_mat.py
def deriv_dihedralangle(u, v, w, i_amo, i_apn, i_aop, xyz):
    d_da = 0

    nu = u / np.linalg.norm(u) #normalize vectors
    nv = v / np.linalg.norm(v)
    nw = w / np.linalg.norm(w)

    sin_theta_u = np.sqrt(1-(np.dot(nu,nw))**2) 
    sin_theta_v = np.sqrt(1-(np.dot(nv,nw))**2)
    cos_theta_u = np.dot(nu, nw) 
    cos_theta_v = np.dot(-nv, nw)

    d_da = (i_amo * (np.cross(nu, nw)[xyz]/(np.linalg.norm(u)*(sin_theta_u**2))) # equation to calculate dDA/dx [1]
    + i_apn * (np.cross(nv,nw)[xyz]/(np.linalg.norm(v)*(sin_theta_v**2))) 
    + i_aop * (((np.cross(nu, nw)[xyz]*cos_theta_u)/(np.linalg.norm(w)*(sin_theta_u**2))) 
    + ((np.cross(nv, nw)[xyz]*cos_theta_v)/(np.linalg.norm(w)*(sin_theta_v**2)))))

    return d_da
