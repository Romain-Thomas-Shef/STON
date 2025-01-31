"""
This file is part of the STON project (P.I. E. Dammer)
it contains the functions to adjust 
sharpness/contrast/brightness/color of the image


Author: R. Thomas
Place: U. of Sheffield
Year: 2025-
"""

#Standard Library


#Third party
from PIL import ImageEnhance
from skimage import filters


#Local import


def color(image_data, factor):
    '''
    This function modifies color of the image data
    
    Parameters
    ----------
    image_data  :   ImageFile
                    data of the image
                    (from 'Image.open(image)')
    factor      :   float
                    from 0.0 to 1.0

    Return
    ------
    modified_data   :   
    '''
    ##Create the enhancer
    enhancer = ImageEnhance.Color(image_data)

    if  0 <= factor <= 500:
        ##Applied the factor (to be divided by 100 because
        ##values of the slider are between 0 and 100)
        modified_data = enhancer.enhance(factor/100)
    else:
        modified_data = image_data

    return modified_data


def contrast(image_data, factor):
    '''
    This function modifies contrast of the image data
    
    Parameters
    ----------
    image_data  :   ImageFile
                    data of the image
                    (from 'Image.open(image)')
    factor      :   float
                    from 0.0 to 1.0

    Return
    ------
    modified_data   :   
    '''
    ##Create the enhancer
    enhancer = ImageEnhance.Contrast(image_data)

    if 0 <= factor <= 500:
        ##Applied the factor (to be divided by 100 because
        ##values of the slider are between 0 and 100)
        modified_data = enhancer.enhance(factor/100)
    else:
        modified_data = image_data

    return modified_data

def sharpness(image_data, factor):
    '''
    This function modifies sharpness of the image data
    
    Parameters
    ----------
    image_data  :   ImageFile
                    data of the image
                    (from 'Image.open(image)')
    factor      :   float
                    from 0.0 to 1.0

    Return
    ------
    modified_data   :   
    '''
    ##Create the enhancer
    enhancer = ImageEnhance.Sharpness(image_data)

    if 0 <= factor <= 500:
        ##Applied the factor (to be divided by 100 because
        ##values of the slider are between 0 and 100)
        modified_data = enhancer.enhance(factor/100)
    else:
        modified_data = image_data

    return modified_data

def brightness(image_data, factor):
    '''
    This function modifies brightness of the image data
    
    Parameters
    ----------
    image_data  :   ImageFile
                    data of the image
                    (from 'Image.open(image)')
    factor      :   float
                    from 0.0 to 1.0

    Return
    ------
    modified_data   :   
    '''
    ##Create the enhancer
    enhancer = ImageEnhance.Brightness(image_data)

    if 0 <= factor <= 500:
        ##Applied the factor (to be divided by 100 because
        ##values of the slider are between 0 and 100)
        modified_data = enhancer.enhance(factor/100)
    else:
        modified_data = image_data

    return modified_data


def gaussian_filter(image_data, sigma):
    '''
    This function applies an image filter

    Parameter
    ---------
    image_data :    numpy array
                    data image

    sigma       :   float
                    sigma of the gaussian filter
    
    Return
    ------
    filtered    :   numpy array
                    image with gaussian filter applied

    '''
    filtered = filters.gaussian(image_data, sigma=sigma)

    return filtered
