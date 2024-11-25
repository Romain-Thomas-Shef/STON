"""
This file is part of the STON project (P.I. E. Dammer)
It contains the functions related to file exploration


Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
version: 0.1

changelog:
----------
0.1 : RTh - Creation
"""
###standard library
import os

###Third party library
from PIL import Image
from PySide6 import QtGui

def create_icon(data, image, item):
    '''
    This function creates an icon to be displayed in the main window
    display area and cluster window dsplay area

    Parameters
    ----------
    data:   bytes
            data from image (from make_thumbnail_from_image function)

    image:  PIL.image object
            data from image (from make_thumbnail_from_image function)

    item    :   QListWidgetItem
                where we put the icon

    return
    ------
    item    :   QlistWiggetItem
                with an Icon
    '''
    ###convert to QImages and then Pixmap
    qim = QtGui.QImage(data, image.size[0], image.size[1],
                             QtGui.QImage.Format.Format_RGBA8888)
    pix = QtGui.QPixmap.fromImage(qim)
    ##Create the Icon
    icon = QtGui.QIcon()
    icon.addPixmap(pix)
    item.setIcon(pix)

    return item


def make_thumbnail_from_image(name_and_path, downgrade_factor):
    '''
    This function open the original image and transform
    it so a thumbnail

    Parameters
    ----------
    name_and_path   :   str
                        name of the image with its path
    downgrade_factor    :   float
                            downgrade factor to apply to the original image
    Return
    ------
    data            :   bytes
                        image to be turned to Icon
    im              :   PIL.Image
                        Thumbnail
    '''
    ###open the file
    image = Image.open(name_and_path)

    ##reduce size (no need to have full resolution for the list of image)
    im = image.thumbnail((image.size[0]/downgrade_factor, image.size[1]/downgrade_factor))

    ##apply color
    im = image.convert("RGBA")

    ##convert to bytes (that's what QT needs)
    data = im.tobytes("raw", "RGBA")

    return data, im


def make_mashup(config, imageswithpath):
    '''
    This function creates a mashup from different images

    Parameters
    ----------
    Config  :   dict
                configuration of the mashup.

    imageswithpath:   list
                    of files with path

    Return
    ------
    mashupimage     str
                    path to new image
    '''
    ##retrieve the images with their path
    fullpath_images = {}
    for image in imageswithpath:
        for configimage in config:
            if configimage == os.path.basename(image):
                fullpath_images[image] = config[configimage]

    ##sort the dictionary
    sorted_images_by_order = sorted(fullpath_images, key=fullpath_images.get)

    ##load the images
    images = []
    for image in sorted_images_by_order:
        images.append(Image.open(image))

    ##get the sizes
    all_width = []
    all_height = []
    for i in images:
        all_width.append(i.size[0])
        all_height.append(i.size[1])

    ##final size
    total_width = sum(all_width)
    total_height = max(all_height)


    #create an empty image
    final_im = Image.new('RGB', (total_width, total_height))

    ##and finally the mashup
    x_offset = 0
    for i in images:
        final_im.paste(i, (x_offset, 0))
        x_offset += i.size[0]

    ###save the image
    final_name = os.path.join(os.path.dirname(imageswithpath[0]), config['name'])
    final_im.save(final_name)

    return final_name
