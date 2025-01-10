'''
This file contains the tests for STON/ston/utils/explore_files.py
'''

###standard library
import os
import unittest

###Third party library


###local imports
from ston.utils import conf


#####define some variable that we will use everywhere
data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                              'test_data')

class conf_get_default_conf(unittest.TestCase):
    '''
    This is the class where the tests are defined
    for the function 'default_conf'
    '''
    def test_default_conf(self):
        '''
        A simple call to the function and we test the output
        '''
        ##Call the function
        default = conf.default_conf()

        #Check the default configuration 
        self.assertEqual(default['Project_info']['name'], 'to_be_changed')
        self.assertEqual(default['Project_info']['extensions'],\
                        ['*.tif', '*.png', '*.jpeg', '*.JPG', '*.JPEG', '*.jpg'])


        self.assertEqual(default['Conf']['main_window_width'], 1150)
        self.assertEqual(default['Conf']['main_window_height'], 700)
        self.assertEqual(default['Conf']['zoom_window_width'], 900)
        self.assertEqual(default['Conf']['zoom_window_height'], 400)
        self.assertEqual(default['Conf']['zoom_insert_pix_size'], 50)
        self.assertEqual(default['Conf']['cluster_window_width'], 900)
        self.assertEqual(default['Conf']['cluster_window_height'], 400)
        self.assertEqual(default['Conf']['compare_window_width'], 900)
        self.assertEqual(default['Conf']['compare_window_height'],400)

        self.assertEqual(default['General_image_display']['image_width'], 200)
        self.assertEqual(default['General_image_display']['downgrade_factor'], 10)


        self.assertEqual(default['Meta_image_options']['downgrade_factor'], 10)
        self.assertEqual(default['Meta_image_options']['ncol_meta_image'], 3)
        self.assertEqual(default['Meta_image_options']['meta_txt_fontsize'], 25)
        self.assertTrue(default['Meta_image_options']['name_on_images'])

class conf_get_load_conf(unittest.TestCase):
    '''
    This is the class where the tests are defined
    for the function 'load_conf'. The previous class
    where we test the default conf is already calling
    that function so we 'only' going to test what is modified
    'manually' by the code.
    ''' 

    test_conf = os.path.join(data_directory, 'test.conf') 

    def test_a_check_sections(self):
        '''
        Test that all section are there
        '''
        ##Call the function
        loaded, _ = conf.load_conf(self.test_conf)

        ##The configuration is turn to a dictionary
        ##so we just need to check the keys
        expected = ['Project_info', 'Conf', 'General_image_display',
                    'Meta_image_options']
        retrieved = list(loaded.keys())
        
        self.assertCountEqual(expected, retrieved)

    def test_b_test_extension_list(self):
        '''
        Test for different list of extensions
        '''
        ##Call the function
        loaded, msg = conf.load_conf(self.test_conf)

        ###test that the message is correct
        self.assertEqual(msg, 'Configuration file found')

        ####Test some things we changed
        self.assertEqual(loaded['Project_info']['name'], 'test_conf')
        self.assertCountEqual(loaded['Project_info']['extensions'], ['*.tif', '*.fits', '*.jpeg'])  
        self.assertFalse(loaded['Meta_image_options']['name_on_images'])
        

   
