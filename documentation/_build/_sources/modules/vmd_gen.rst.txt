===============
Module: vmd_gen
===============

This script generates a VMD readable output. 
VMD colors bonds according to the strain energy stored in them (green: low strain, yellow: medium
strain, red: high strain; transitions are fluent). 

In the case of the bond lengths, this procedure is straightforward. 
The energy stored in the bond angles and dihedral angles,
on the other hand, is split between the bonds involved in the given coordinate and finally
the different contributions for each bond are added up. Moreover, the region that stores
the highest amount of stress energy in a given type of coordinate is always colored red,
regardless whether this is a high or low percentage of the overall molecular strain. 

In default, the VMD Analysis only displays H, C, N, O and S. It is possible to add one or more atoms that should be displayed in the VMD Analysis. 
For this, specify them as individual lines with their RGB values in a file vmd_add.txt. 
For adding Ti atoms, for example, vmd_add.txt would look like this: 

Ti 0.5 0.5 0.5