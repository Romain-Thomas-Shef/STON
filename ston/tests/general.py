'''
This file gather all the tests to be run

It is called via the command --test on the cli
'''
####Standard library
import unittest

####Third party


###Local imports
from . import test_utils_explore_files
from . import test_utils_conf
from . import test_utils_cli
from . import test_open_save_files


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


