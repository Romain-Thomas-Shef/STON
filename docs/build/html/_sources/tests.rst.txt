Testing STON
============

STON is fully testable. STON development fully separated the GUI from the back-end functions.
You can test both separately. 


Back-end functions
------------------
To test the backend part of STON you need to use the terminal and the command line interface (see :doc:`get_started`)::

    [me@mymachine]: ston --test

Here it will ask you what you want to test::

    [me@mymachine]: ston --test
    What test do you want to run?
    [utils/processing, just press enter for all]:

You can either press enter for the full test suite or write `utils` or `processing` to test some parts only. 
This part of the testing uses the ``unittest`` module, part of the standard library.


You can also use ``pytest``. For this you must go to the installation directory of STON and run ``pytest ston/tests/``.


A few details:

* ``utils``: This will test everything that deals with finding files, saving/opening txt files, reading configuration. So far there are **21** tests implemented.
* ``processing``: This will test everything that deal with images.


Graphical Interface
-------------------



