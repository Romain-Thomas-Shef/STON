'''
This file contains the tests for STON/ston/processing/image_processing.py
'''

###standard library
import os
import unittest

###Third party library
from PIL import Image
import numpy

###local imports
from ston.processing import image_processing

###Some useful variables
data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                              'test_data')

class TestContrastAndAverageColor(unittest.TestCase):
    '''
    This is the class where the tests are defined
    for the function 'most_contrasted_color' and 'compute_avg_color'
    '''

    def test_1_avg_black_image(self):
        '''
        Test that the average of a black image is black
        '''
        ##Create a black image
        black = Image.new('RGB', (100, 100), color = (0,0,0))

        ###compute avg
        rgb = image_processing.compute_avg_color(numpy.array(black))

        ##And test
        self.assertEqual(rgb, (0, 0, 0))

    def test_2_avg_white_image(self):
        '''
        Test that the average color of a white image is white
        '''
        ##Create a white image
        white = Image.new('RGB', (100, 100), color = (255,255,255))

        ###compute avg
        rgb = image_processing.compute_avg_color(numpy.array(white))

        ##And test
        self.assertEqual(rgb, (255, 255, 255))

    def test_3_black_image(self):
        '''
        Get font color for a completely black image
        (we should get white)
        '''
        ##Create a black image
        black = Image.new('RGB', (100, 100), color = (0,0,0))

        ##get average color
        rgb = image_processing.compute_avg_color(numpy.array(black))

        ##compute most contrasted image
        font_color = image_processing.most_contrasted_color(rgb)

        ##And test
        self.assertEqual(font_color, (255, 255, 255))

    def test_4_white_image(self):
        '''
        Get font color for a completely white image
        (we should get black)
        '''
        ##Create a white image
        white = Image.new('RGB', (100, 100), color = (255, 255, 255))

        ##get average color
        rgb = image_processing.compute_avg_color(numpy.array(white))

        ##compute most contrasted image
        font_color = image_processing.most_contrasted_color(rgb)

        ##And test
        self.assertEqual(font_color, (0, 0, 0))



class MASHUP(unittest.TestCase):
    '''This class tests the function 'make_mashup'
    '''

    def test_mashup_a_single(self):
        '''
        The mashup of a single image is the image itself
        '''
        ##Get an image
        image = os.path.join(data_directory, 'cluster1_1sthalf/1-ker-ppl.jpg')

        ##Create a configuration
        conf = {}
        conf['name'] = 'testmashup.png'
        conf['1-ker-ppl.jpg'] = '1'

        ##create a mashup
        name = image_processing.make_mashup(conf, [image])

        ###test the output of the function
        self.assertEqual(name, conf['name'])

        ##Reload the image that was created
        imagecreated = numpy.array(Image.open(conf['name']))

        ##Load the single image
        original_image = numpy.array(Image.open(image))

        ##Check both image are similar
        self.assertTrue(numpy.array_equal(original_image, imagecreated))

        ##remove the created image
        os.remove(conf['name'])

    def test_mashup_b_two_images(self):
        '''
        The mashup of two images
        '''
        ##Get an image
        image1 = os.path.join(data_directory, 'cluster1_1sthalf/1-ker-ppl.jpg')
        image2 = os.path.join(data_directory, 'cluster1_1sthalf/2-ker-ppl.jpg')

        ##we load the manualy create double image
        doublemashup = os.path.join(data_directory, 'testdoublemashup_manual.png')

        ##Create a configuration
        conf = {}
        conf['name'] = 'testmashupdouble.png'
        conf['1-ker-ppl.jpg'] = '1'
        conf['2-ker-ppl.jpg'] = '2'

        ##create a mashup
        name = image_processing.make_mashup(conf, [image1, image2])

        ##Reload the image that was created
        imagecreated = numpy.array(Image.open(name))

        ##Load the single image
        manual_mashup = numpy.array(Image.open(doublemashup))

        ##Check both image are similar
        self.assertTrue(numpy.array_equal(manual_mashup, imagecreated))

        ##remove the created image
        os.remove(conf['name'])

    def test_mashup_c_three_images_difsizes(self):
        '''
        The mashup of three images with different sizes
        '''
        ##Get an image
        image1 = os.path.join(data_directory, 'cluster1_1sthalf/1-ker-ppl.jpg')
        image2 = os.path.join(data_directory, 'nested/2nd_level/3rd_level/singletif/TS-ceramic.tif')
        image3 = os.path.join(data_directory, 'cluster1_1sthalf/2-ker-ppl.jpg')

        ##we load the manualy create double image
        triplemashup = os.path.join(data_directory, 'testtriple_manual.png')

        ##Create a configuration
        conf = {}
        conf['name'] = 'testmashuptriple.png'
        conf['1-ker-ppl.jpg'] = '1'
        conf['TS-ceramic.tif'] = '2'
        conf['2-ker-ppl.jpg'] = '3'

        ##create a mashup
        name = image_processing.make_mashup(conf, [image1, image2, image3])

        ##Reload the image that was created
        imagecreated = numpy.array(Image.open(name))

        ##Load the manual made image
        manual_mashup = numpy.array(Image.open(triplemashup))

        ##Check both image are the same
        self.assertTrue(numpy.array_equal(manual_mashup, imagecreated))

        ##remove the created image
        os.remove(conf['name'])


class META(unittest.TestCase):
    '''This class tests the function 'create_meta_image'
    '''

    def test_meta_a_single_image(self):
        '''
        A meta image of a single image is just the image
        with its name on top of it and with the gaps
        '''
        ##Get an image
        image = os.path.join(data_directory, 'cluster1_1sthalf/1-ker-ppl.jpg')

        ##Create a configuration
        conf = {}
        conf['Meta_image_options'] = {}
        conf['Meta_image_options']['downgrade_factor'] = 10
        conf['Meta_image_options']['name_on_images'] = True
        conf['Meta_image_options']['ncol_meta_image'] = 1
        conf['Meta_image_options']['meta_txt_fontsize'] = 10

        ##final image name
        final_image_name = 'meta_image_single_image.png'

        ###make the meta image
        image_processing.create_meta_image([image], final_image_name, conf)

        ###open it back
        final_image = Image.open(final_image_name)

        ###open the test image
        test_image = Image.open(os.path.join(data_directory,
                                             'test_meta_1image_with_text.png'))


        print(final_image.size, test_image.size)

        ##Check both image are the same
        self.assertTrue(numpy.array_equal(numpy.array(final_image),
                                          numpy.array(test_image)))

        ##remove the created image
        os.remove(final_image_name)

    def test_meta_b_single_image_noname(self):
        '''
        A meta image of a single image is just the image
        Here we do not add the name to the image
        '''
        ##Get an image
        image = os.path.join(data_directory, 'cluster1_1sthalf/1-ker-ppl.jpg')

        ##Create a configuration
        conf = {}
        conf['Meta_image_options'] = {}
        conf['Meta_image_options']['downgrade_factor'] = 10
        conf['Meta_image_options']['name_on_images'] = False
        conf['Meta_image_options']['ncol_meta_image'] = 1
        conf['Meta_image_options']['meta_txt_fontsize'] = 10

        ##final image name
        final_image_name = 'meta_image_single_image_noname.png'

        ###make the meta image
        image_processing.create_meta_image([image], final_image_name, conf)

        ###open it back
        final_image = Image.open(final_image_name)

        ###open the test image
        test_image = Image.open(os.path.join(data_directory,
                                             'test_meta_1image_with_text_noname.png'))

        ##Check both image are the same
        self.assertTrue(numpy.array_equal(numpy.array(final_image),
                                          numpy.array(test_image)))

        ##remove the created image
        os.remove(final_image_name)

    def test_meta_c_three_image_2_columns(self):
        '''
        A meta image of three images in a column is the two image
        on the top line and one on the bottom line
        '''
        ##Get an image
        image = os.path.join(data_directory, 'cluster1_1sthalf/1-ker-ppl.jpg')
        image2 = os.path.join(data_directory, 'nested/2nd_level/3rd_level/singletif/TS-ceramic.tif')
        image3 = os.path.join(data_directory, 'cluster1_1sthalf/3-ker-ppl.jpg')

        ##Create a configuration
        conf = {}
        conf['Meta_image_options'] = {}
        conf['Meta_image_options']['downgrade_factor'] = 10
        conf['Meta_image_options']['name_on_images'] = True
        conf['Meta_image_options']['ncol_meta_image'] = 2
        conf['Meta_image_options']['meta_txt_fontsize'] = 10

        ##final image name
        final_image_name = 'meta_image_three_image_2column.png'

        ###make the meta image
        image_processing.create_meta_image([image, image2, image3],
                                            final_image_name, conf)
        ###open it back
        final_image = Image.open(final_image_name)

        ###open the test image
        test_image = Image.open(os.path.join(data_directory,
                                             'test_meta_threeimage_2columns.png'))

        print(final_image.size, test_image.size)

        ##Check both image are the same
        self.assertTrue(numpy.array_equal(numpy.array(final_image),
                                          numpy.array(test_image)))

        ##remove the created image
        os.remove(final_image_name)
