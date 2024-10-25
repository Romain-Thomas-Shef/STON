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
###Third party library
from PIL import Image

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
