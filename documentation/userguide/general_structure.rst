==========
User Guide
==========

The JEDI Analysis requires redundant internal coordinates, where as the input data is 
given in cartesian coordinates.  

General structure
-----------------

The main routine ``jedi.py`` runs all the subscripts in the following order: 

1.  Read x0, xF and the Hessian (``jedi_files.py``)
2.  Calculate the redundant internal modes from the relaxed geometry (``jedi_rims.py``)
3.  Check if atoms are to be masked (``jedi_kill_atoms.py``)
4.  Calculate the B-Matrix (``jedi_b.py``)
5.  Convert the change in cartesian coordinates into redundant internal coordinates (``jedi_delta_q.py``)
6.  Run the JEDI Analysis