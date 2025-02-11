Testing STON
============

STON can be tested *relatively* easily. STON development fully separated the GUI from the back-end functions.
You can test both separately. 

Back-end functions
------------------
To test the backend part of STON you need to use the terminal and the command line interface (see :doc:`get_started`)::

    [me@mymachine]: ston --test

Here it will ask you what you want to test::

    [me@mymachine]: ston --test
    What test do you want to run?
    [utils/processing/segmentation, just press enter for all]:

You can either press enter for the full test suite or write `utils` or `processing` to test some parts only. 
This part of the testing uses the ``unittest`` module, part of the standard library.


You can also use ``pytest``. For this you must go to the installation directory of STON and run ``pytest ston/tests/``.


A few details:

* ``utils``: This will test everything that deals with finding files, saving/opening txt files, reading configuration.
* ``processing``: This will test everything that deal with images creation (mashup, metaimage, etc). 


Graphical Interface
-------------------

We did not write unittests for the graphical interface. Instead we have stored *test data* in the package and you can follow the following procedure to test the main functionalities of the interface. 

To start the GUI in test mode just use the following command::

    [me@mymachine]: ston --config test

When starting, STON will start two windows: the :doc:`main_window` and the :doc:`zoom_window` window.

Main window
^^^^^^^^^^^

The :doc:`main_window` should give you access to the following data (on the left file explorer):

* singletif --> 1 image
* logo --> 1 image 
* cluster1_1sthalf --> 5 images
* 3rd_level --> 4 images
* cluster2 --> 10 images
* cluster1_2ndhalf --> 5 images

If you deploy the *3rd_level* directory, and double click on **ceramic3.jpg** and **ceramic2.jpg**, images will be displayed on the right part of the window. You should have the following window at this point:

.. figure:: /images/GUI/test_GUI_main_window.png
   :width: 700
   :align: center

   Main window of STON with **ceramic3.jpg** and **ceramic2.jpg** open on the display area

Zoom window
^^^^^^^^^^^

If you double click on **ceramic3.jpg** in the image area, you can go to the second window (the detail window), you should see this:

.. figure:: /images/GUI/test_GUI_detail_window.png
   :width: 700
   :align: center

   Detail window on the with **ceramic3.jpg** image loaded.


Passing the mouse over the image, you will see the closeup window on the bottom left showing a zoom in part of the region where mouse is (see the short video in :doc:`zoom_window`). You can see that there are already some notes on the notepad. These are the notes displayed for testing purpose. You might modify this notes and save them back (**Note:** it will be saved only if the directory where ston is saved is available with write rights).


Analysis window
^^^^^^^^^^^^^^^


Cluster window
^^^^^^^^^^^^^^


Side by side comparison
^^^^^^^^^^^^^^^^^^^^^^^
