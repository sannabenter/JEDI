=======
Hessian
=======

The Hessian can be calculated via a standard frequency calculation. 
The wrapper script ``hess_gen.py`` supports Q-Chem and ORCA.

The script is to be executed with the following command line input:

.. code-block:: console

    python hess_gen.py <input_file.out> <program>

* <input_file.out> : name of the file containing the geometry 
* <program> : program that generated the output (either Q_Chem or ORCA)