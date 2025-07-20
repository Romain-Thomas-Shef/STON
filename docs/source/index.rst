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



What is STON and why did we do it?
==================================

Thin-section petrography is a widely used technique in archaeology for analyzing the composition of ceramic and stone objects, as well as investigating their production technology and provenance (`Reedy, 2008 <https://books.google.nl/books?id=t1ErAQAAIAAJ>`; `Peterson & Betancourt, 2009 <https://www.jstor.org/stable/j.ctt3fgvbq>`; `Quinn, 2022 <https://books.google.nl/books?id=b7B1EAAAQBAJ>`). 
This method involves studying these materials in thin sections mounted on glass slides under a polarizing microscope to examine their microscopic features. A critical aspect of archaeological study is the comparison and identification of patterns within these features across multiple samples.
However, it is typically only possible to view one sample at a time under the microscope. As a result, this method relies heavily on visual memory and repeated observations, making the process inefficient and time-consuming, particularly when dealing with hundreds of samples.

This tool is designed to address these challenges by enabling users to observe multiple photomicrographs simultaneously within a single, convenient interface. It facilitates detailed comparisons, clustering, and data recording, which is especially important in ceramic paste analysis.
By allowing users to view multiple samples side by side, the software supports efficient sample grouping and evaluation of compositional characteristics.

While tailored for the specific requirements of petrographic analysis in archaeology, the software has broader applications in other research fields that rely on visual image analysis.
By providing an efficient and scalable tool for comparative analysis, it enhances research processes across various disciplines.


How to navigate the documentation?
==================================

.. figure:: /images/frontpage/screenshot_main_window.png
   :width: 400
   :align: right

   Main window of STON

If you are new to STON and would like to install the software you can look at the dedicated page on :doc:`installation`. To understand how to start STON and configure the software, please have a look at :doc:`get_started`. Finally, if you want to have a look at the documentation for the different windows you can have a look at :doc:`main_window`, :doc:`zoom_window`, :doc:`cluster_window` and :doc:`comparison_window`.  


----

**Contribute:**
If you find a bug or would like to propose a new feature, we would appreciate if you could write an issue in the `github <https://github.com/Romain-Thomas-Shef/STON>`_ repository. If you want to start a general discussion you can also use the `github discussion <https://github.com/Romain-Thomas-Shef/STON/discussions>`_ and engage with us and others.
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
