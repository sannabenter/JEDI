============================
Module: JEDI - main routine
============================

The main routine imports all subscripts. It converts the Hessian in 
redundant internal coordinates and calculates the energy in every 
internal mode using the equation shown below.

.. math:: E_{RIMs} = \frac{1}{2} * {\Delta q}^T * H_q * \Delta q 

The main routine produces the output discussed in the 
`output section <https://jedi-analysis.readthedocs.io/en/latest/userguide/output.html>`_.