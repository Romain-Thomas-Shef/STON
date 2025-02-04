"""
This file is part of the STON project (P.I. E. Dammer)
It contains the code for segmentation and region identification

Author: R. Thomas
Place: U. of Sheffield
Year: 2025-
"""

#Standard Library


#Third party
import numpy
from skimage import filters, segmentation, measure


#Local import


def apply_sobel(image_data):
    '''
    This function applies the sobel filter to
    the input image
    
    Parameters
    ----------
    image_data  :   numpy array
                    data of the image


    Return
    ------
    edges      : numpy array
                 filtered image   
    '''
    edges = filters.sobel(image_data)
    #edges = segmentation.chan_vese(image_data)

    return edges

def apply_chan_vese(image_data):
    '''
    This function applies the chan vese segmentation to
    the input image
    
    Parameters
    ----------
    image_data  :   numpy array
                    data of the image


    Return
    ------
    segmentation     : numpy array
                       segmentated image   
    '''
    ##grayscale
    data = image_data[:,:,0] 
    segm = segmentation.chan_vese(data)

    npix = numpy.shape(data)[0] * numpy.shape(data)[1]

    ##get some data: count the number of white and black pixels
    black = len(numpy.where(segm == 0)[0])/npix
    white = len(numpy.where(segm == 1)[0])/npix

    ##result
    r = {}
    r['black'] = round(black, 2)
    r['white'] = round(white, 2)

    return segm, r


def find_regions(image_data):
    '''
    This method uses the label function from skimage
    to find connected region

    Parameters
    ----------
    image_data  :   numpy array
                    data of the image

    '''
    
    image_data = image_data[:,:,0] 
    npix = numpy.shape(image_data)[0] * numpy.shape(image_data)[1]

    ##To find region we need to create a binary_image
    ##we set the threshold at image image
    binary_image = image_data > numpy.mean(image_data)
    
    ##Label connected regions
    labeled_image = measure.label(binary_image)

    ##Measure properties of labeled regions
    properties = measure.regionprops(labeled_image)

    ##keep only the properties we want
    scatter_x = []
    scatter_y = []
    region_area = []
    region_bbox = []
 
    for region in properties:
        x, y = region.centroid
        scatter_x.append(x)
        scatter_y.append(y)
        region_area.append(region.area)
        region_bbox.append(region.bbox)
    
    results = {'x': scatter_x, 'y': scatter_y, 'region': region_area,
               'bbox': region_bbox}


    labeled_image[labeled_image>0] = 1
    #labeled_image = 1 - labeled_image

    ##get some data: count the number of white and black pixels
    black = len(numpy.where(labeled_image == 0)[0])/npix
    white = len(numpy.where(labeled_image == 1)[0])/npix

    ##result
    ratios = {}
    ratios['black'] = round(black, 2)
    ratios['white'] = round(white, 2)

    return labeled_image, results, ratios
