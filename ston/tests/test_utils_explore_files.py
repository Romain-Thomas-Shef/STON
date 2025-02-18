'''
This file contains the tests for STON/ston/utils/explore_files.py

Author: R. Thomas
Place: U. of Sheffield, RSE team
Year: 2024-2025
'''

###standard library
import os
import unittest

###Third party library


###local imports
from ston.utils import explore_files


#####define some variable that we will use everywhere
data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                              'test_data')
extensions = ['.tif', '.jpg', '.png', 'FITS']


class ExploreGetDirAndFiles(unittest.TestCase):
    '''
    This is the class where the tests are defined
    for the function 'get_dir_and_files'
    '''
    def test_1_directories_multiext(self):
        '''
        Check that all directories with files with matching extension
        are found
        '''
        ##Call the function
        file_dict = explore_files.get_dir_and_files(data_directory, extensions)

        ##Expected list of directories with files
        expected = ['cluster1_1sthalf', 'cluster1_2ndhalf',
                    '3rd_level', 'cluster2', 'singletif', 'test_data',
                    'dummy_analysis'] 


        ###Make a bit of cleanup
        received = []
        for key, _ in file_dict.items():
            received.append(os.path.basename(key))

        ###Check that expected and received is the same
        ###The order does not matter
        self.assertCountEqual(expected, received)

    def test_2_files_multiext(self):
        '''
        Check that the files are the expected one. Test with multiple extensions
        '''
        ##Call the function
        file_dict = explore_files.get_dir_and_files(data_directory, extensions)

        ##Expected files in some directories with files
        expected_cluster1_1sthalf = ['1-ker-ppl.jpg', '2-ker-ppl.jpg', '3-ker-ppl.jpg',
                                     '4-ker-ppl.jpg', '5-ker-ppl.jpg']
        corresponding_dir = os.path.join(data_directory, 'cluster1_1sthalf')

        ###and test
        self.assertCountEqual(file_dict[corresponding_dir], expected_cluster1_1sthalf)

        ###try one deep in the subdirectories
        expected_singletif = ['TS-ceramic.tif']
        corresponding_dir = os.path.join(data_directory, 'nested/2nd_level/3rd_level/singletif')
        self.assertCountEqual(file_dict[corresponding_dir], expected_singletif)


    def test_3_directory_single_ext(self):
        '''
        Try with only one extension (in that case .tif)
        '''
        ##Call the functinn
        file_dict = explore_files.get_dir_and_files(data_directory, [extensions[0]])

        ###Check that only one directory is found
        self.assertEqual(len(file_dict.keys()), 1)

        ###And check that it is correct
        self.assertEqual(os.path.basename(list(file_dict.keys())[0]), 'singletif')

    def test_4_directory_single_ext(self):
        '''
        Try with only one extension (in that case .jpg)
        '''
        ##Call the functinn
        file_dict = explore_files.get_dir_and_files(data_directory, [extensions[1]])

        ###Check that 4 directories are found
        self.assertEqual(len(file_dict.keys()), 5)


    def test_5_directory_wrong_ext(self):
        '''
        Try with only one extension where no files are available
        '''
        ##Call the function
        file_dict = explore_files.get_dir_and_files(data_directory, [extensions[-1]])

        ###Check we get an empty directory
        self.assertFalse(file_dict)


    def test_6_empty_directory(self):
        '''
        Test that when there is not image with matching extension
        the function returns an empty dict
        '''
        ###create the path to an empty dict
        empty_dict = os.path.join(data_directory, 'nested/test_empty')

        ###Call the function
        file_dict = explore_files.get_dir_and_files(empty_dict, extensions)

        ###check that we have an empty dict
        self.assertFalse(file_dict)

class TestGetFilesAndPath(unittest.TestCase):
    '''
    This is the class where the tests are defined
    for the function 'get_files_and_path'
    '''
    ###prepare the file_dict
    file_dict = explore_files.get_dir_and_files(data_directory, extensions)

    def test_a_noignore_singlefile(self):
        '''
        No ignore files, simple list of 1 file
        '''
        ##prepare expected output
        expected_file_no_path = ['TS-ceramic.tif']
        relative_path = 'nested/2nd_level/3rd_level/singletif/TS-ceramic.tif'
        expected_file_with_path = [os.path.join(data_directory, relative_path)]

        ##call the function
        file_with_path,\
                file_no_path = explore_files.get_files_and_path(['TS-ceramic.tif'],
                                                                self.file_dict, [])

        ##And check
        self.assertCountEqual(expected_file_no_path, file_no_path)
        self.assertCountEqual(expected_file_with_path, file_with_path)

    def test_b_noignore_2files_indifdirectory(self):
        '''
        Same as before but with two files located in different directories
        '''

        ##prepare expected output
        expected_file_no_path = ['TS-ceramic.tif', '5-ker-ppl.jpg']
        relative_path = 'nested/2nd_level/3rd_level/singletif/TS-ceramic.tif'
        relative_path2 = 'cluster1_1sthalf/5-ker-ppl.jpg'
        expected_file_with_path = [os.path.join(data_directory, relative_path),
                                   os.path.join(data_directory, relative_path2)]

        ##call the function
        file_with_path,\
            file_no_path = explore_files.get_files_and_path(['TS-ceramic.tif', '5-ker-ppl.jpg'],
                                                            self.file_dict, [])

        ##And check
        self.assertCountEqual(expected_file_no_path, file_no_path)
        self.assertCountEqual(expected_file_with_path, file_with_path)

    def test_c_no_files_selected(self):
        '''
        test that when no files are selected we get two empty lists
        '''
        ##prepare expected output
        expected_file_no_path = []
        expected_file_with_path = []

        ##call the function
        file_with_path, file_no_path = explore_files.get_files_and_path([], self.file_dict, [])

        ##And check
        self.assertCountEqual(expected_file_no_path, file_no_path)
        self.assertCountEqual(expected_file_with_path, file_with_path)



    def test_d_with_ignore_files(self):
        '''
        Same as test 8 but we ask to ignore one of the file
        '''
        ##prepare expected output
        expected_file_no_path = ['TS-ceramic.tif']
        relative_path = 'nested/2nd_level/3rd_level/singletif/TS-ceramic.tif'
        expected_file_with_path = [os.path.join(data_directory, relative_path)]

        ##call the function
        file_with_path,\
            file_no_path = explore_files.get_files_and_path(['TS-ceramic.tif', '5-ker-ppl.jpg'],
                                                             self.file_dict, ['5-ker-ppl.jpg'])

        ##And check
        self.assertCountEqual(expected_file_no_path, file_no_path)
        self.assertCountEqual(expected_file_with_path, file_with_path)
