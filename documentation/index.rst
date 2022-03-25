
========================================================================
Welcome to JEDI, the Judgement of Energy Distribution Analysis
========================================================================

The JEDI Analysis (Judgement of Energy Distribution Analysis) is a quantum chemical force analysis tool for the distribution of stress
energy in a mechanically deformed molecule. JEDI is developed in Python. Currently, the main contributor to JEDI is the `Institute for physical and theoretical Chemistry 
<https://www.uni-bremen.de/institut-fuer-physikalische-und-theoretische-chemie>`_, 
respectively the `AG Neudecker <https://www.uni-bremen.de/ag-neudecker/>`_ of the University of Bremen (https://www.uni-bremen.de/). 

Introduction and Overview
=========================
Based on the harmonic approximation, the JEDI Analysis calculates the strain energy for each bond, bending and torsion in a molecule, thus allowing the
identification of the mechanically most strained regions in a molecule as well as the rationalization of mechanochemical processes.


Usage
======

JEDI can be used in three different applications.

Mechanically deformed Molecules
-------------------------------
When a molecule is stretched, some internal modes store more energy than others. 
This leads to particularly large displacements of certain modes and to the preconditioning 
of selected bonds for rupture. Using the JEDI analysis the mechanochemical properties can be investigated.

Excited State 
-------------
Besides the description of mechanical deformation in the ground state, the JEDI
analysis can be used in the electronically excited state to quantify the energy gained by
relaxation on the excited state potential energy surface (PES). For this, the harmonic
approximation needs to be applicable on the excited state PES of interest. The physical
process that is described by the excited state JEDI analysis is fundamentally different
from the ground state variant. While in the ground state JEDI analysis the distribution of
stress energy in a mechanically deformed molecule is analyzed, i.e. energy is expended for
deformation, the excited state JEDI analysis quantifies the energy gained by the relaxation
of each internal mode upon relaxation on the excited state PES, i.e. energy becomes
available.


Adsorbed molecules
------------------
The JEDI analysis allows force analysis for a subset of atoms. Thus, it is applicable to calculate the strain that builds up within an 
adsorbation of a molecule onto a surface. It is possible to mask the surface using the kill_atoms script. 

Installation
=============

.. toctree::
   :maxdepth: 1
   :caption: Installation:

   installation/prerequisites_compilation


Preparation
=============

.. toctree::
   :maxdepth: 1
   :caption: Preparation:
   
   preparation/hess_gen
   preparation/energies_gen
   preparation/geometries_gen


Package / Module Documentation
==============================

.. toctree::
    :maxdepth: 1
    :caption: User Guide    

    usersguide/general_structure

.. toctree::
   :maxdepth: 1
   :caption: Modules

   modules/module_overview
   modules/jedi_files
   modules/jedi_directory
   modules/jedi_rims
   modules/jedi_primitives
   modules/jedi_kill_atoms
   modules/jedi_b
   modules/jedi_delta_q
   modules/jedi


Indices and tables
==================

* :ref:`genindex`
