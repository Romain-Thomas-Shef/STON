Installation
============

Dependencies
------------
STON is written entirely in Python. To make it work you will neec the following packages:

* PySide6: This the graphical interface library. We coded it using version 6.8.0.1
* Pillow and numpy : This is what allows us to manipulate images and data. We used Pillow version 11.1.0 and number version 2.2.1.
* matplotlib: this is what we use to display images (version 3.10.0)
* scikit-image: For region identification, version 0.25.0

.. danger::

    We advise you to create a dedicated python environment when you install STON. See `here <https://docs.python.org/3/library/venv.html>`_ for more details.


Install from pip
----------------

.. note:: 

    Coming soon!



Install from github
-------------------

To install from github you can:

* Clone the `repository <https://github.com/Romain-Thomas-Shef/STON>`_ and create a local install from it
* Use pip to install it directly from github:

.. code-block:: shell

    pip install git+https://github.com/Romain-Thomas-Shef/STON
