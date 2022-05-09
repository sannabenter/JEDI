=================
Module: jedi_rims
=================

This script converts cartesian coordinates (from x0.txt) into redundant internal modes. 
It creates three files containing the internal modes: 

* bl.txt - containing all the bonds
* ba.txt - containing all the bond angles
* da.txt - containing all the torsion angles

To define the bond lengths in a molecule, a database [1] is imported containing the 
average covalent radius of every element. 
The molecule is mapped by calculating all atomic distances. 
The covalent radii of the involved atoms are summed to define the theoretical 
bond length of the considered bond. 
Within a threshold of 0.3 a.u. bonds are defined by comparing the 
atomic distances and the sum of the covalent radii.

The bond and torsion angles are defined along the bonds.

[1] B. Cordero, V. Gomez, A. Platero-Prats, et. al Dalton Trans., 2008, 2832–2838