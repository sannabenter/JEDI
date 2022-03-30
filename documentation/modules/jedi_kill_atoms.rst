=======================
Module: jedi_kill_atoms
=======================

This routine is implemented to mask surface atoms in adsorbate-asorbant-systems. 
The atoms need to be defined in the according jedi_kill_atoms_input.txt file. 

The ``jedi_kill_atoms`` script reads jedi_kill_atoms_input.txt to generate list of to be deleted atoms. 
It deletes atoms from the Hessian (H_Cart.txt), the redundant internal coordinates (bl.txt, ba.txt and da.txt) and the geometry-files (x0.txt and xF.txt).