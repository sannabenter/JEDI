==========
User Guide
==========

The JEDI Analysis produces output and performs the underlying calculations in redundant internal coordinates, 
where as the input data is given in cartesian coordinates. The main routine of the JEDI Analysis converts the 
cartesian coordinates and the Hessian into redundant internal coordinates to then apply the
harmonic approximation to calculate the energies in the redundant internal coordinates.
To achieve the switching between the cartesian and redundant internal coordinates, the B-Matrix is calculated according to 
V. Bakken, T. Helgaker, J. Chem. Phys. 117 (20) 2002. 

General structure
-----------------

The main routine ``jedi.py`` runs all subscripts in the following order: 

1.  Read x0, xF, energies and the Hessian (``jedi_files.py``)

2.  Calculate the redundant internal modes of the relaxed geometry (``jedi_rims.py``)

3.  Check if atoms are defined to be masked (``jedi_kill_atoms.py``)

4.  Calculate the B-Matrix (``jedi_b.py``)

5.  Convert the change in cartesian coordinates into redundant internal coordinates (``jedi_delta_q.py``)

6.  Run the JEDI Analysis


Optional Arguments
------------------

The main routine ``jedi.py`` takes two optional arguments.

Specify a directory
...................
By calling a ``--d`` flag a path can be specified, that already contains a 
list of redundant internal modes. 

.. code-block:: console

    jedi.py --d <directory_path>

Generate VMD Output
...................

By default the JEDI Analysis generates a VMD readable output, which defines bonds colors
according to the strain energy stored in them (green: low strain, yellow: medium
strain, red: high strain; transitions are fluent).

The --v flag can be either used to suppress the vmd_gen.py script or to manually specify
a maximum strain that is colored "reddest" in the VMD Analysis.

.. code-block:: console

    jedi.py --v n/maximum_strain

For further information on the ``--d`` or ``--v`` flag, please take a closer look into the according modules. 





