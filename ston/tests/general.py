'''
This file gather all the tests to be run

It is called via the command --test on the cli

Author: R. Thomas
Place: U. of Sheffield, RSE team
Year: 2024-2025
'''
####Standard library
import unittest

####Third party


###Local imports
from . import test_utils_explore_files
from . import test_utils_conf
from . import test_utils_cli
from . import test_open_save_files
from . import test_processing_image_processing
from . import test_segmentation

def run_tests(tests='all'):
    '''
    This function run the tests of STON

    Parameters
    ----------
    tests   :   str
                default=all and run all the tests
                other options are available:
                utils
                processing
                GUI

    Return
    ------
    None 
    '''
    print(50*'-'+'start testing\n\n')

    if tests in ['all', 'utils']:
        print(50*'-')
        print('We run the tests for the modules under ston/utils')
        print(50*'-')

        ####ston/utils/explore_files.py
        suite = unittest.TestLoader().loadTestsFromModule(test_utils_explore_files)
        unittest.TextTestRunner(verbosity=2).run(suite)

        ####ston/utils/conf.py
        print('\n')
        suite = unittest.TestLoader().loadTestsFromModule(test_utils_conf)
        unittest.TextTestRunner(verbosity=2).run(suite)

        ####ston/utils/cli.py
        print('\n')
        suite = unittest.TestLoader().loadTestsFromModule(test_utils_cli)
        unittest.TextTestRunner(verbosity=2).run(suite)

        ####ston/utils/open_saves_file.py
        print('\n')
        suite = unittest.TestLoader().loadTestsFromModule(test_open_save_files)
        unittest.TextTestRunner(verbosity=2).run(suite)


    if tests in ['all', 'processing']:
        print('ok')
        ####ston/processing/image_processing.py
        print('\n')
        suite = unittest.TestLoader().loadTestsFromModule(test_processing_image_processing)
        unittest.TextTestRunner(verbosity=2).run(suite)

    if tests in ['all', 'segmentation']:
        print('ok')
        ####ston/processing/segmentation_region.py
        print('\n')
        suite = unittest.TestLoader().loadTestsFromModule(test_segmentation)
        unittest.TextTestRunner(verbosity=2).run(suite)


