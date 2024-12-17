Development corner
==================


Git repo structure
------------------

STON is stored in `github <https://github.com/Romain-Thomas-Shef/STON>`_. The structure of the repository is the following:


.. code-block:: shell

     STON/
     ├── docs/
     │   ├── build/
     │   ├── index.html
     │   ├── make.bat
     │   ├── Makefile
     │   └── source/  # where to edit the documentation
     ├── LICENCE.txt
     ├── pyproject.toml # Python Packaging configuration file
     ├── README.md  # github README
     ├── ston/ # Where the source code is
     ├── test/ # Where the tests are


If you want to edit the source code you must go in the subdirectory called **ston**. The documentation can be edited under **docs/source**.


Source code flow
----------------

To understand a bit how the structure of the code works you can look at the picture below.

.. figure:: images/Dev_corner/STON.png
   :width: 600
   :align: center

   Source code flow

The *pyproject.toml* file includes the ``[project.scripts]`` section with ``ston="ston.main:main"``. This means that when you start STON with the ``ston`` command it will go directly in the *main.py* file starting the ``main()`` function. 
This function is parsing the command line interface argument that were given by the user. Depending on these, STON will do multiple actions:

- Create an empty configuration file (``makeconfig``). This is done directly in the *main.py* function.
- Display the version of STON (``--version``).
- Start the main window (``--config`` or no arguments at all). This will extract first a configuration (done in *conf.py*):

  - If no argument was passed, a default configuration will be given,
  - if a configuration is passed, it is read and extracted.

Once a configuration is ready, the ``main()`` function calls the ``GUI()`` class from *main_windows.py* file. This is where the main window is coded. This code is calling various local modules: 

- The other windows:
  
  - *zoom_window.py*: This is where the window with an image, header diplayer and live zoom window is displayed
  - *comparison_window.py*: where two images can be viewed side by side.
  - *cluster_window.py*: where multiple images can be grouped.
 
- *explore_files.py*: where we find files in the disk
- *image_processing.py*: where the images are modified for display.


The content of ``ston/`` is visible below:

.. code-block:: shell

        ston
        ├── GUI
        │   ├── cluster_window.py
        │   ├── comparison_window.py
        │   ├── logo
        │   │   └── logo.jpeg
        │   ├── main_window.py
        │   └── zoom_window.py
        ├── __init__.py
        ├── main.py
        ├── processing
        │   ├── explore_files.py
        │   └── image_processing.py
        ├── pylintrc
        ├── template_file
        ├── tests
        └── utils
            ├── cli.py
            ├── conf.py
            ├── example.conf
            └── __init__.py

You can see that extra files/directories are available:

* *pylintrc*: this is the pylint configuration file for STON.
* *template_file*: This is a file with just a header. To start a new source code file.
* *example.conf*: This is the generic configuration file used by the ``--makeconfig`` argument. 


Documentation
-------------

.. note::

   If you want to edit the documentation, you will need to install ``sphinx`` and ``sphinx-rtd-theme``. 

All the documentation is written in **docs/**. To edit it you need to go to source and edit the file you want to modify. Everything is written in `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_ markup language. 

Once modified, go to **docs/** and run ``make clean && make html`` in the terminal. This will erase the previous version and create a new version of the documentation with your modifications.

.. danger:: 

   To be able to update the github documentation, you need to compile it first in your disk and then push everything in the repo.

Linting
-------

.. note::

   To lint locally you need to install Pylint 3.0.3

Linting of the code is done automatically via a `github-action <https://github.com/Romain-Thomas-Shef/STON/blob/main/.github/workflows/pylint.yml>`_. It uses `pylint <https://pylint.readthedocs.io/en/stable/whatsnew/3/3.0/>`_ 3.0.3 with the *pylintrc* file available in the source code. The github action will fail if the pylint score falls below 9/10. This github action is triggered ONLY if some of the source code a been changed (i.e. if you just change the documentation it will not be triggered).

If you want to lint the code localy you can run the following command ``pylint --rcfile=pylintrc your_file.py``, where *pylintrc* is the file in the source code directory.
