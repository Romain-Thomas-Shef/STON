'''
This file contains the tests for STON/ston/utils/cli.py
'''

###standard library
import unittest

###Third party library

###local imports
from ston.utils import cli


class command_line(unittest.TestCase):
    '''
    This is the class where the tests are defined
    for the function 'comand_line_interface'
    '''
    def test_1_noargs(self):
        '''
        Simulate the response of the cli when the user does not
        use any argument
        '''
        ##Call the function
        parsed = cli.command_line_interface([])

        ##check arguments
        self.assertFalse(parsed['tests']) 
        self.assertEqual(parsed['config'], 'default')
        self.assertFalse(parsed['makeconfig'])

    
    def test_2_makeconfig(self):
        '''
        Use of makeconfig args
        '''
        ##Call the function
        parsed = cli.command_line_interface(['--makeconfig'])

        ##check arguments
        self.assertFalse(parsed['tests']) 
        self.assertEqual(parsed['config'], 'default')
        self.assertTrue(parsed['makeconfig'])

    def test_3_config(self):
        '''
        Use of config args
        '''
        ##Call the function
        parsed = cli.command_line_interface(['--config', 'test'])

        ##check arguments
        self.assertFalse(parsed['tests']) 
        self.assertEqual(parsed['config'], 'test')
        self.assertFalse(parsed['makeconfig'])


