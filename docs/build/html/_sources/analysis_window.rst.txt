Analysis window
================

Description of the window
-------------------------

The analysis window allows you to segment images and identify regions of interest in the image. When opened, it will display the same image as in the :doc:`zoom_window` window:

.. figure:: images/GUI/analyse_window_with_annotations.png
   :width: 700
   :align: center

   Analysis window


The analysis window is composed of the following areas:
* Tabs (pink): This is where you will see images. It is always displaying the tab 'Image to analyse' at first. The other tabs (region plot, region histogram, explore regions) are all empty. At the bottom of each tab you will see the *matplotlib* toolbar (in red). This allows you to zoom in/out, save the image.


* The initial image tuning (yellow): A few button to tune what image will be analyse. It can be cropped and a gaussian filter can be applied to the image (see below).

* The analysis information box (green). Each time something is done in that window, information will be displayed on that box. You can clear it or save the text using the buttons at the bottom. 

* Running the algotirhm (blue): This is the button you need to hit for STON to make the analysis


Cropping and Gaussian filtering
-------------------------------

Cropping
^^^^^^^^

In some case you might want to remove areas of the image. To make this easy we implemented a cropping option. 
To crop an image you must use the lense button at the bottom of the window (in the ref box in the screenshot), then select an area in the image. 
Once the image has been zoom to this area  you must use the button *Crop Image*. This will ensure that the image that will be analysed will be the cropped one. To uncrop the image and revert back to the original image, use the *Reset to original* button.



Gaussian filtering
^^^^^^^^^^^^^^^^^^

It might be useful, if you want the smallest regions to not be identified, to use a gaussian filter in the image. The spinbox next to the button *Gaussian filtering* allows you to choose the sigme of the filter. When hitting the button, the filter will be applied to the displayed window:

.. figure:: images/Analysis/gaussian.jpg
    :width: 900
    :align: center 

    Example of Gaussian filtering

.. note:: If you use the button while the displayed image is already filtered, the gaussian filter will be applied to that filtered image. Make sure you reload the image with *Reset to Original* or *Reset to cropped* before applying again a Gaussian filter.

The gaussian filtering used here is the one of skimage (see `here <https://scikit-image.org/docs/dev/api/skimage.filters.html#skimage.filters.gaussian>`_).

Identifying region and visualisation
------------------------------------


