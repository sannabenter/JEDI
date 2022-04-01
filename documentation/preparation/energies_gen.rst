========
Energies
========

To compare the ab initio energies and the energy calculated with the harmonic approximation, 
the JEDI Analysis takes an E_geoms.txt file containing the ab initio energies. 
``energies_gen.py`` extracts the energies from the DFT calculation files. 

Use the wrapper script with: 

.. code-block:: console

    python energies_gen.py <opt_file> <force_opt_file> <program> 

* <opt_file> : name of the file containing the relaxed geometry 
* <force_opt_file> : name of the file containing the strained geometry; possible input files: 
Single Point Calculation or Geometry Optimization 
* <program> : program that generated the output (either Q_Chem or ORCA)

.. warning:: 
    This wrapper script only works for Single Point Calculations of the strained molecule. 


