'''
This file contains the tests for STON/ston/processing/image_processing.py
'''

###standard library
import os
import unittest

###Third party library
import numpy
from PIL import Image

###local imports
from ston.processing import segmentation_regions

###Some useful variables
dummy_image = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                           'test_data/test_segmentation.png')

dummy_image2 = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                           'test_data/test_segmentation2.png')

class Testsegmentation(unittest.TestCase):
    '''
    This is the class where the tests are defined
    for the function 'find_regions'
    '''

    def test_1_default_conf_on_dummy(self):
        '''
        Load the dummy image and a default conf
        '''
        ##Open the dummy
        dummy = numpy.array(Image.open(dummy_image))

        ##Create a configuration
        conf = {}
        conf['Analysis'] = {'minimum_size':2}

        ##call the function
        labeled, results = segmentation_regions.find_regions(dummy, conf)
        del labeled

        ##And check the results. The dummy image has only 8 regions
        self.assertEqual(len(results['x']), 8)

        ##as the dummy image is made of colored squared on a black background,
        ##the bbox should have the same size as the area
        ##We check if that's the case for each region (8)
        for i in range(8):
            bbox = (results['bbox'][i][2]-results['bbox'][i][0]) * \
                    (results['bbox'][i][3]-results['bbox'][i][1])
            self.assertEqual(results['area'][i], bbox)

    def test_2_minimum_size(self):
        '''
        Load the dummy image and a conf with a different size
        '''
        ##Open the dummy
        dummy = numpy.array(Image.open(dummy_image))

        ##Create a configuration
        conf = {}
        conf['Analysis'] = {'minimum_size':3000}

        ##call the function
        labeled, results = segmentation_regions.find_regions(dummy, conf)
        del labeled

        ##And check the results. The dummy image has only 8 region and we
        ##remove 2 with a change of minimum size
        self.assertEqual(len(results['x']), 6)

        ##as the dummy image is made of colored squared on a black background,
        ##the bbox should have the same size as the area
        ##We check if that's the case for each region (8)
        for i in range(6):
            bbox = (results['bbox'][i][2]-results['bbox'][i][0]) * \
                    (results['bbox'][i][3]-results['bbox'][i][1])
            self.assertEqual(results['area'][i], bbox)

    def test_3_second_dummy(self):
        '''
        Load the dummy image and a conf with a different size
        '''
        ##Open the dummy
        dummy = numpy.array(Image.open(dummy_image2))

        ##Create a configuration
        conf = {}
        conf['Analysis'] = {'minimum_size':2}

        ##call the function
        labeled, results = segmentation_regions.find_regions(dummy, conf)
        del labeled

        ##And check the results. The dummy image has only 8 region and we
        ##remove 2 with a change of minimum size
        self.assertEqual(len(results['x']), 9)

        ##Check some bbox
        bbox = (results['bbox'][0][2]-results['bbox'][0][0]) * \
               (results['bbox'][0][3]-results['bbox'][0][1])
        self.assertEqual(bbox, 32116)

        bbox = (results['bbox'][-1][2]-results['bbox'][-1][0]) * \
               (results['bbox'][-1][3]-results['bbox'][-1][1])
        self.assertEqual(bbox, 4620)
