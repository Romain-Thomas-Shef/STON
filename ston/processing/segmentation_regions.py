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
from skimage import filters, segmentation, measure, color


#Local import


def find_regions(image_data, conf):
    '''
    This method uses the label function from skimage
    to find connected region

    Parameters
    ----------
    image_data  :   numpy array
                    data of the image

    conf        :   dict
                    configuration of STON

    return
    ------
    labeled     :   numpy array
                    segmented images
    result      :   dict
                    with results
    '''

    #Convert to grayscale 
    image_data = color.rgb2gray(image_data)

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
        if region.area > conf['Analysis']['minimum_size']:
            x, y = region.centroid
            scatter_x.append(x)
            scatter_y.append(y)
            region_area.append(region.area)
            region_bbox.append(region.bbox)

    ##Sort everything from biggest region to smallest
    #First, transfor to numpy array
    region_area = numpy.array(region_area)
    scatter_x = numpy.array(scatter_x)
    scatter_y = numpy.array(scatter_y)
    region_bbox = numpy.array(region_bbox)

    #Then sort the area and the rest
    inds = region_area.argsort()[::-1]
    sorted_x = scatter_x[inds]
    sorted_y = scatter_y[inds]
    sorted_bbox = region_bbox[inds]
    sorted_area = region_area[inds]
    
    
    results = {'x': sorted_x, 'y': sorted_y, 'area': sorted_area,
               'bbox': sorted_bbox}

    labeled_image[labeled_image>0] = 1

    ##result
    ##number of pixel in the image (to compute ratios after)
    npix = numpy.shape(image_data)[0] * numpy.shape(image_data)[1]

    ##get some data: count the number of white and black pixels
    results['black_ratio'] = round(len(numpy.where(labeled_image == 0)[0])/npix, 2)
    results['white_ratio'] = round(len(numpy.where(labeled_image == 1)[0])/npix, 2)

    return labeled_image, results
