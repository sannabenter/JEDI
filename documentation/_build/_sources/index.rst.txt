
========================================================================
Welcome to JEDI-Analysis, the Judgement of Energy Distribution Analysis
========================================================================

The JEDI Analysis (Judgement of Energy Distribution Analysis) is a quantum chemical force analysis tool for the distribution of stress
energy in a mechanically deformed molecule. JEDI is developed in Python. Currently, the main contributor to JEDI is the `Institute for physical and theoretical Chemistry 
<https://www.uni-bremen.de/institut-fuer-physikalische-und-theoretische-chemie>`_, 
respectively the `AG Neudecker <https://www.uni-bremen.de/ag-neudecker/>`_ of the [University of Bremen](https://www.uni-bremen.de/) . 

Introduction and Overview
=========================
Based on the harmonic approximation, the JEDI Analysis calculates the strain energy for each bond, bending and torsion in a molecule, thus allowing the
identification of the mechanically most strained regions in a molecule as well as the rationalization of mechanochemical processes.


--------
Features
--------

JEDI currently provides ... main features: 

-------------------
What JEDI cannot do 
-------------------

elementspezifisch usw.

Installation
=============

.. toctree::
   :maxdepth: 1

   installation/prerequisites_compilation


Preparation
=============

.. toctree::
   :maxdepth: 1
   
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
