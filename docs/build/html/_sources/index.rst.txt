.. STON documentation master file, created by
   sphinx-quickstart on Mon Oct 14 13:26:20 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

STON: SofTware for petrOgraphic visualisatioN
=============================================

.. figure :: images/logo/logo.png
    :align: left
    :width: 200

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
.. image:: https://img.shields.io/badge/python-3.12%2B-blue
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen



What is STON?
=============

Welcome to the documenation of STON. STON is a visualisation tool that you can use if you want to get a better look at petrogrpahic images taken from microscopes. Supporting multiple image formats, it allows you to zoom, compare images side by side, cluster images together etc... 

How to navigate the documentation?
==================================

.. figure:: /images/frontpage/screenshot_main_window.png
   :width: 400
   :align: right

   Main window of STON

If you are new to STON and would like to install the software you can look at the dedicated page on :doc:`installation`. To understand how to start STON and configure the software, please have a look at :doc:`get_started`. Finally, if you want to have a look at the documentation for the different windows you can have a look at :doc:`main_window`, :doc:`zoom_window`, :doc:`cluster_window` and :doc:`comparison_window`.  


----

**Contribute:**
If you find a bug or would like to propose a new feature, we would appreciate if you could write an issue in the `github <https://github.com/Romain-Thomas-Shef/STON>`_ repository.
We also welcome anyone who wants to contribute to the development. If this is your case please have a look at the :doc:`dev_notes` and if you have any question you can write to E. Dammer (dammer.evgenia@gmail.com) and R.Thomas (romain.thomas@sheffield.ac.uk).  




.. warning::

	**Copyright**

	STON is a free software: you can redistribute it and/or modify it under
	the terms of the GNU General Public License as published by the Free Software Foundation,
	version 3 of the License.

	STON is distributed without any warranty; without even the implied warranty of merchantability
	or fitness for a particular purpose.  See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public License along with the program.
	If not, see http://www.gnu.org/licenses/ .

----

Table of content
----------------
.. toctree::
 :maxdepth: 1
 
 installation
 get_started
 main_window
 zoom_window
 analysis_window
 cluster_window
 comparison_window
 tests
 dev_notes
