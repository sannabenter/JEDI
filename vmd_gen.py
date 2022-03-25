import numpy as np
import os.path
import sys
from jedi import directory, man_strain, modus
from jedi_kill_atoms import ls_NrAtoms
import jedi_functions

#########################
#       Basic stuff     #
#########################

# Check whether we need to write vmd_ba.tcl, vmd_da.tcl and vmd_all.tcl and read basic stuff
file_list = []

# Bond lengths (a molecule has at least one bond):
if os.path.exists("bl_manip.txt"):
    bl_file = 'bl_manip.txt'
elif os.path.exists("bl.txt"):
    bl_file = 'bl.txt'
else:
    bl_file = False
if bl_file:
	bl = []
	ins = open(bl_file, 'r')
	for line in ins:
		number_strings = line.split()
		numbers = [int(n) for n in number_strings]
		if len(ls_NrAtoms) > 0:
			for killed_atom in ls_NrAtoms:
				number_1 = jedi_functions.kill_atoms(killed_atom, numbers[0])
				number_2 = jedi_functions.kill_atoms(killed_atom, numbers[1])
				numbers = [number_1, number_2]
		bl.append(numbers)
	open('vmd_bl.tcl', 'w').close()
	file_list.append('vmd_bl.tcl')
else:
	print("Fatal error in vmd-gen.py: File bl.txt not found, so no bonds detected. This can't be right.")
	sys.exit(0)

# Bond angles:
if os.path.exists("ba_manip.txt"):
    ba_file = 'ba_manip.txt'
elif os.path.exists("ba.txt"):
    ba_file = 'ba.txt'
else:
    ba_file = False
if ba_file:
	ba_flag = True
	ba = []
	ins = open(ba_file, 'r')
	for line in ins:
		number_strings = line.split()
		numbers = [int(n) for n in number_strings]
		if len(ls_NrAtoms) > 0:
			for killed_atom in ls_NrAtoms:
				number_1 = jedi_functions.kill_atoms(killed_atom, numbers[0])
				number_2 = jedi_functions.kill_atoms(killed_atom, numbers[1])
				number_3 = jedi_functions.kill_atoms(killed_atom, numbers[2])
				numbers = [number_1, number_2, number_3]
		ba.append(numbers)
	open('vmd_ba.tcl', 'w').close()
	file_list.append('vmd_ba.tcl')
# All (for this, at least bond angles have to be present):
	open('vmd_all.tcl', 'w').close()
	file_list.append('vmd_all.tcl')

# Dihedral angles:
if os.path.exists("da_manip.txt"):
    da_file = 'da_manip.txt'
elif os.path.exists("da.txt"):
    da_file = 'da.txt'
else:
    da_file = False
if da_file:
	da_flag = True
	da = []
	ins = open(da_file, 'r')
	for line in ins:
		number_strings = line.split()
		numbers = [int(n) for n in number_strings]
		if len(ls_NrAtoms) > 0:
			for killed_atom in ls_NrAtoms:
				number_1 = jedi_functions.kill_atoms(killed_atom, numbers[0])
				number_2 = jedi_functions.kill_atoms(killed_atom, numbers[1])
				number_3 = jedi_functions.kill_atoms(killed_atom, numbers[2])
				number_4 = jedi_functions.kill_atoms(killed_atom, numbers[3])
				numbers = [number_1, number_2, number_3, number_4]
		da.append(numbers)
	open('vmd_da.tcl', 'w').close()
	file_list.append('vmd_da.tcl')
else:
	da_flag = False

# E_RIMs_perc
if os.path.isfile('E_RIMs_perc.txt') == True:
	E_RIMs_perc = np.loadtxt('E_RIMs_perc.txt')
else:
	print("Fatal error in vmd-gen.py: File E_RIMs_perc.txt not found, so no energies detected. This can't be right.")

# Write some basic stuff to the tcl scripts
for filename in file_list:
	if filename == "vmd_bl.tcl" or filename == "vmd_ba.tcl" or filename == "vmd_da.tcl" or filename == "vmd_all.tcl":
		f = open(filename, 'w')
		f.write('# Load a molecule\nmol new geom.xyz\n\n')
		f.write('# Change bond radii and various resolution parameters\nmol representation cpk 0.8 0.0 30 5\nmol representation bonds 0.2 30\n\n')
		f.write('# Change the drawing method of the first graphical representation to CPK\nmol modstyle 0 top cpk\n')
		f.write('# Color only H atoms white\nmol modselect 0 top {name H}\n')
		f.write('# Change the color of the graphical representation 0 to white\ncolor change rgb 0 1.00 1.00 1.00\nmol modcolor 0 top {colorid 0}\n')
		f.write('# The background should be white ("blue" has the colorID 0, which we have changed to white)\ncolor Display Background blue\n\n')
		f.write('# Define the other colorIDs\n')
		f.close()

# Define colorcodes for various atomtypes
colors = [['C', 0.5, 0.5, 0.5],
['N', 0.0, 0.0, 1.0],
['O', 1.0, 0.0, 0.0],
['S', 1.0, 1.0, 0.0]]

N_standard_colors = len(colors)
N_colors = 32 - N_standard_colors # VMD allows 32 colors in total, leaving 28 colors to remain, when subtracting the 4 color codes for the atoms defined above 

# Check whether the user has defined to color more atoms than standard atoms and adjust N_colors accordingly
if os.path.exists("vmd_add.txt"):
	N_colors2add = 0
	file = open ('vmd_add.txt', 'r')
	atoms2add = []

	for line in file.readlines():
		y = [value for value in line.split()]
	# The line should contain the atom name (field 0) and the RGB code (fields 1-3) that the user has specified
	# Check whether the user has specified this correctly and, if yes, decrement N_colors		
		try:
			float(y[0])
			print("Fatal error in vmd-gen.py Please use the proper formatting in vmd_add.txt.")
			sys.exit(0)
		except ValueError:
			pass
		except IndexError:
			print("Fatal error in vmd-gen.py Please use the proper formatting in vmd_add.txt.")
			sys.exit(0)
		try:
			float(y[1])
			float(y[2])
			float(y[3])
		except ValueError:
			print("Fatal error in vmd-gen.py Please use the proper formatting in vmd_add.txt.")
			sys.exit(0)
		except IndexError:
			print("Fatal error in vmd-gen.py Please use the proper formatting in vmd_add.txt.")
			sys.exit(0)

		atoms2add.append( y )
		N_colors -= 1
	file.close()

N_colors2add = 28 - N_colors # remaining 27 colors after subtracting the 4 color codes for the atoms defined above (s. line 97)

# Generate the color-code and write it to the tcl scripts
for filename in file_list:
	if filename == "vmd_bl.tcl" or filename == "vmd_ba.tcl" or filename == "vmd_da.tcl" or filename == "vmd_all.tcl":
		f = open(filename, 'a')

		for i in range(N_colors):
			R_value = float(i)/(N_colors/2)
			if R_value > 1:
				R_value = 1

			if N_colors % 2 == 0:
				G_value = 2 - float(i+1)/(N_colors/2)
			if N_colors % 2 != 0:
				G_value = 2 - float(i)/(N_colors/2)
			if G_value > 1:
				G_value = 1

			B_value = 0

			f.write('%1s%4i%10.6f%10.6f%10.6f%1s' % ("color change rgb", i+1, R_value, G_value, B_value, "\n"))

		# add color codes of "standard" atoms
		for j in range(N_standard_colors):
			f.write('%1s%4i%10.6f%10.6f%10.6f%1s' % ("color change rgb", N_colors+j+1, float(colors[j][1]), float(colors[j][2]), float(colors[j][3]), "\n"))
		if os.path.isfile('vmd_add.txt') == True:
			for i in range(N_colors2add):
				f.write('%1s%4i%10.6f%10.6f%10.6f%1s' % ("color change rgb", N_colors+i+1, float(atoms2add[i][1]), float(atoms2add[i][2]), float(atoms2add[i][3]), "\n"))

		for j in range(N_standard_colors):
			f.write('\n\nmol representation cpk 0.7 0.0 30 5')
			f.write('\nmol addrep top') 	
			f.write('\n%s%i%s' % ("mol modstyle ", j+1, " top cpk"))
			f.write('\n%s%i%s%i%s' % ("mol modcolor ", j+1, " top {colorid ", N_colors+j+1, "}"))
			f.write('\n%s%i%s%s%s' % ("mol modselect ", j+1, " top {name ", colors[j][0], "}"))
		
		if os.path.isfile('vmd_add.txt') == True:
			for i in range(N_colors2add):
				f.write('\n\nmol representation cpk 0.7 0.0 30 5')
				f.write('\nmol addrep top')
				f.write('\n%s%i%s' % ("mol modstyle ", i+1, " top cpk"))
				f.write('\n%s%i%s%i%s' % ("mol modcolor ", i+1, " top {colorid ", N_colors+i+1, "}"))
				f.write('\n%s%i%s%s%s' % ("mol modselect ", i+1, " top {name ", atoms2add[i][0], "}"))
		f.close()


#########################
#	Binning		#
#########################

# Welcome
print("\n\nCreating tcl scripts for generating color-coded structures in VMD...")

# Achieve the binning for bl, ba, da an all simultaneously
sum_energy = 0  # variable to add up all energies in the molecule
for filename in file_list:
	if filename == "vmd_bl.tcl" or filename == "vmd_ba.tcl" or filename == "vmd_da.tcl" or filename == "vmd_all.tcl":

# Create an array that stores the bond connectivity as the first two entries. The energy will be added as the third entry.
		bond_E_array = np.zeros([len(bl),3])
		for i in range(len(bl)):
			bond_E_array[i][0] = bl[i][0]
			bond_E_array[i][1] = bl[i][1]

# Create an array that stores only the energies in the coordinate of interest and print some information
# Get rid of ridiculously small values and treat diatomic molecules explicitly
# (in order to create a unified picture, we have to create all these arrays in any case)
# Bonds
		if filename == "vmd_bl.tcl" or filename == "vmd_all.tcl":
			if len(bl) == 1:
				E_bl_perc = E_RIMs_perc
			else:
				E_bl_perc = E_RIMs_perc[0:len(bl)]
				if E_bl_perc.max() <= 0.001:
					E_bl_perc = np.zeros(len(bl))
			if filename == "vmd_bl.tcl":
				print("\nProcessing bond lengths...")
				print("%s%6.2f%s" % ("Maximum energy in a bond length:      ", E_bl_perc.max(), '%'))
				print("%s%6.2f" % ("Total energy in the bond lengths:     ", E_bl_perc.sum()))

# Bendings
		if (filename == "vmd_ba.tcl" and ba_flag == True) or (filename == "vmd_all.tcl" and ba_flag == True):
			E_ba_perc = E_RIMs_perc[len(bl):len(bl)+len(ba)]
			if E_ba_perc.max() <= 0.001:
				E_ba_perc = np.zeros(len(ba))
			if filename == "vmd_ba.tcl":
				print("\nProcessing bond angles...")
				print("%s%6.2f%s" % ("Maximum energy in a bond angle:       ", E_ba_perc.max(), '%'))
				print("%s%6.2f" % ("Total energy in the bond angles:      ", E_ba_perc.sum()))

# Torsions (handle stdout separately)
		if (filename == "vmd_da.tcl" and da_flag == True ) or (filename == "vmd_all.tcl" and da_flag == True):
			E_da_perc = E_RIMs_perc[len(bl)+len(ba):len(bl)+len(ba)+len(da)]
			if E_da_perc.max() <= 0.001:
				E_da_perc = np.zeros(len(da))
		if filename == "vmd_da.tcl" and da_flag == True:
			print("\nProcessing dihedral angles...")
			print("%s%6.2f%s" % ("Maximum energy in a dihedral angle:   ", E_da_perc.max(), '%'))
			print("%s%6.2f" % ("Total energy in the dihedral angles:  ", E_da_perc.sum()))

# Map onto the bonds (create "all" on the fly and treat diatomic molecules explicitly)
# Bonds (trivial)
		if filename == "vmd_bl.tcl" or filename == "vmd_all.tcl":
			for i in range(len(bl)):
				if len(bl) == 1:
					bond_E_array[i][2] = E_bl_perc
				else:
					bond_E_array[i][2] = E_bl_perc[i]
		
					
# Bendings
		if (filename == "vmd_ba.tcl" and ba_flag == True) or (filename == "vmd_all.tcl" and ba_flag == True):
			for i in range(len(ba)):
				for j in range(len(bl)):
					if ((ba[i][0] == bl[j][0] and ba[i][1] == bl[j][1]) or  # look for the right connectivity
					    (ba[i][0] == bl[j][1] and ba[i][1] == bl[j][0]) or
					    (ba[i][1] == bl[j][0] and ba[i][2] == bl[j][1]) or
					    (ba[i][1] == bl[j][1] and ba[i][2] == bl[j][0])):
						bond_E_array[j][2] += 0.5 * E_ba_perc[i]

# Torsions
		if (filename == "vmd_da.tcl" and da_flag == True) or ( filename == "vmd_all.tcl" and da_flag == True ):
			for i in range(len(da)):
				for j in range(len(bl)):
					if ((da[i][0] == bl[j][0] and da[i][1] == bl[j][1]) or 
					    (da[i][0] == bl[j][1] and da[i][1] == bl[j][0]) or
					    (da[i][1] == bl[j][0] and da[i][2] == bl[j][1]) or
					    (da[i][1] == bl[j][1] and da[i][2] == bl[j][0]) or
					    (da[i][2] == bl[j][0] and da[i][3] == bl[j][1]) or
					    (da[i][2] == bl[j][1] and da[i][3] == bl[j][0])):
						bond_E_array[j][2] += (float(1)/3) * E_da_perc[i]
		
	
# Store the maximum energy in a variable for later call
		if filename == "vmd_all.tcl":
			if not modus == "all":  # only do this, when the user didn't call the --v flag 
				max_energy = float(np.amax(bond_E_array, axis=0)[2])  # maximum energy in one bond
				for row in bond_E_array: 
					if max_energy in row:
						atom_1_max_energy = int(row[0])
						atom_2_max_energy = int(row[1])

# Generate the binning windows by splitting bond_E_array into N_colors equal windows
	if filename == "vmd_all.tcl":
		if modus == "all":
			if man_strain == None:
				print(f"modus {modus} was called, but no maximum strain is given.")
				binning_windows = np.linspace( 0, np.amax(bond_E_array, axis=0)[2], num=N_colors )
			else:
				binning_windows = np.linspace( 0, float(man_strain), num=N_colors )
		else: 
			binning_windows = np.linspace( 0, np.amax(bond_E_array, axis=0)[2], num=N_colors )
	
	elif filename == "vmd_bl.tcl":
		if modus == "bl":
			if man_strain == None:
				print(f"modus {modus} was called, but no maximum strain is given.")
				binning_windows = np.linspace( 0, np.amax(bond_E_array, axis=0)[2], num=N_colors )
			else:
				binning_windows = np.linspace( 0, float(man_strain), num=N_colors )
		else: 
			binning_windows = np.linspace( 0, np.amax(bond_E_array, axis=0)[2], num=N_colors )

	elif filename == "vmd_ba.tcl":
		if modus == "ba":
			if man_strain == None:
				print(f"modus {modus} was called, but no maximum strain is given.")
				binning_windows = np.linspace( 0, np.amax(bond_E_array, axis=0)[2], num=N_colors )
			else:
				binning_windows = np.linspace( 0, float(man_strain), num=N_colors )
		else: 
			binning_windows = np.linspace( 0, np.amax(bond_E_array, axis=0)[2], num=N_colors )

	elif filename == "vmd_da.tcl":
		if modus == "da":
			if man_strain == None:
				print(f"modus {modus} was called, but no maximum strain is given.")
				binning_windows = np.linspace( 0, np.amax(bond_E_array, axis=0)[2], num=N_colors )
			else:
				binning_windows = np.linspace( 0, float(man_strain), num=N_colors )
	else: 
		binning_windows = np.linspace( 0, np.amax(bond_E_array, axis=0)[2], num=N_colors )

# Calculate which binning_windows value is closest to the bond-percentage and do the output
	f = open(filename, 'a')
	f.write("\n\n# Adding a representation with the appropriate colorID for each bond")

	for i in range(len(bl)):
		colorID = np.abs( binning_windows - bond_E_array[i][2] ).argmin() + 1
		f.write('\nmol addrep top')
		f.write('\n%s%i%s' % ("mol modstyle ", N_standard_colors+i+N_colors2add+1, " top bonds"))
		f.write('\n%s%i%s%i%s' % ("mol modcolor ", N_standard_colors+i+N_colors2add+1, " top {colorid ", colorID, "}"))
		f.write('\n%s%i%s%i%s%i%s' % ("mol modselect ", N_standard_colors+i+N_colors2add+1, " top {index ", bond_E_array[i][0]-1, " ", bond_E_array[i][1]-1, "}\n"))
	f.close()
		
# if not man_strain:  # only do this, when the user didn't call the --v flag 
# 	print("\nAdding all energies for the stretch, bending and torsion of the bond with maximum strain...")
# 	print(f"Maximum energy in bond between atoms {atom_1_max_energy} and {atom_2_max_energy}: {float(max_energy):.2f} hartree.")
