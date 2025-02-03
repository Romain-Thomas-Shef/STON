'''
This file contains the tests for STON/ston/utils/cli.py

Author: R. Thomas
Place: U. of Sheffield, RSE team
Year: 2024-2025
'''

###standard library
import os
import unittest
from pathlib import Path

###Third party library

###local imports
from ston.utils import open_save_files

#####define some variable that we will use everywhere
data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                              'test_data')

class Open(unittest.TestCase):
    '''
    This is the class where the tests are defined
    for the function 'open_txt_file'
    '''
    ##The file we will read
    test_conf = os.path.join(data_directory, 'test.conf')

    def test_1_fileexist(self):
        '''
        Test the behavior of the function if the file we want to read
        exists
        '''
        ##We can read whatever txt file
        ##so we are just going to read a conf file
        txt = open_save_files.open_txt_file(self.test_conf)

        ###Split line by line
        splittxt = txt.strip().split('\n')

        ##check a few lines:
        firstline = '#This is an example of configuration file'
        lastline = 'name_on_images = No'

        ##And test that it is what we extracted with the function
        self.assertEqual(firstline, splittxt[0])
        self.assertEqual(lastline, splittxt[-1])

    def test_2_file_doesnot_exist(self):
        '''
        Test the behavior of the function if the file does not exist
        '''
        ##so we are just going to read a conf file
        txt = open_save_files.open_txt_file('test_nofile')

        ###And test the output
        expected = 'The file was not found'
        self.assertEqual(txt, expected)


class Save(unittest.TestCase):
    '''
    This is the class where the tests are defined
    for the function 'open_txt_file'
    '''
    ##The file we will save
    savefile = os.path.join(os.getcwd(), 'testfile_ston.txt')

    def test_a_goodfile_and_text(self):
        '''
        Test the behavior of the function if the directory where
        we want to save the file exists and if there is some text
        '''
        ##We can read whatever txt file
        ##so we are just going to read a conf file
        text = 'Help\nplease\nwe are stuck!!!'
        open_save_files.save_txt_to_file(self.savefile, text)

        ##read it back
        txt_read = open_save_files.open_txt_file(self.savefile)

        ##And check
        self.assertEqual(txt_read, text)

        ###FInally we need to remove the file that was saved
        os.remove(self.savefile)

    def test_b_goodfile_and_notxt(self):
        '''
        Test the behavior of the function if the directory where
        we want to save the file exists and if there is NO text
        '''
        ##We can read whatever txt file
        ##so we are just going to read a conf file
        txt = open_save_files.save_txt_to_file(self.savefile, '')

        ##and check
        expected = 'No text was passed....we did not save a file'
        self.assertEqual(expected, txt)

    def test_c_badfile_and_goodtxt(self):
        '''
        Test the behavior of the function if the directory where
        we want to save the file does not exists and if there is good text
        '''
        ##We can read whatever txt file
        ##so we are just going to read a conf file
        text = 'Help\nplease\nwe are stuck!!!'

        ###make a wrong file
        savefiledir = os.path.join(Path.home(), 'unexistingdir')
        savefile = os.path.join(savefiledir, 'text.txt')
        txt = open_save_files.save_txt_to_file(savefile, text)

        ##and check
        expected = f'Directory {savefiledir} does not exist...File not saved'
        self.assertEqual(expected, txt)
