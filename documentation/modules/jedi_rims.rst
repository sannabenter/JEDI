=================
Module: jedi_rims
=================

This script converts cartesian coordinates (from x0.txt) into redundant internal modes. 
It creates three files containing the internal modes: 

bl.txt - containing all the bonds
ba.txt - containing all the bondangles
da.txt - containing all the torsionangles

Bond lengths
------------

To define the bond lengths in a molecule, a database is imported containing the 
average covalent radius of every element. 
The molecule is mapped by calculating all atomic distances. 
The covalent radii of the involved atoms are summed to define the theoretical 
bond length of the considered bond. 
Within a threshold of 0.3 a.u. bonds are defined by comparing the 
atomic distances and the sum of the covalent radii.


Bond angles
-----------

Bond angles are defined along the bonds.
