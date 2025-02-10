Individual image visualisation
==============================

Description of the window
-------------------------

.. figure:: /images/zoom_window/Screenshot_with_annotation.png
   :width: 700
   :align: center

   Detailed image window of STON


This image allows you to have a detailed view of an image. When you double click on an image in the :doc:`main_window`, it will then be displayed at the center of this window. From top-left to bottom right, this image shows:

* The **header** display: This *only* works for *.tif* images. Pngs, jpegs or jpg are not supported. 
* Below the header, you can see the **close up image**.  This image shows a subset of the loaded images. To control the section of the image that is displayed in the close up box, just move the mouse over the loaded image at the center of the window:  

.. figure:: /images/GUI/closeup.gif
   :width: 500
   :align: center

   Example of closeup visualisation


Two parameters control what you see in the box and they can be modified in the configuration file (see :doc:`get_started`):
* ``closeup_window``: if set to *original*, this box will always display the original image. If set to *enhanced*, it will display the image as controlled by the enhancers (see below).
* ``closeup_window_size``: This control the size (in pixel) of the box (the box is a square).

* At the center of the window: the loaded image
* Below the loaded image are the **enhancers** controlling some image properties (see last section below).
* On the right of the window you can find the **notepad** and the **Save Notes** button (see next section).


Notepad
-------

The right part of the window is the **notepad**. This is where you can take notes about the image you are seeing.
If you want to save these notes you must hit the **Save Notes** button. If you do that, a new file will be created on disk. Assuming the loaded image is named *image.tif*, a note file will be created in the same directory with the name *image_ston_notes.txt*. 

.. note:: It is important to note that if, for a given image, a note file exists next to the image file, it will be automatically loaded in the notepad. This will allow you to continue your notes.


Image Enhancers
---------------

At the bottom of the window, four **enhancers** are available. They allow you to modify the image adjusting the *color*, *contrast*, *brightness* and *sharpness*. 

To reset the image to its original state you must use the button **Reset Properties**, on the bottom left.
