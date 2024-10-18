"""
This file is part of the STON project (P.I. E. Dammer)
It loads the configuration of the tool.
if no configuration was given, it will load an empty one
if one was given it will extract configuration from it.

Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
version: 0.1

changelog:
----------
0.1 : RTh - Creation
"""

###Python standard library
import configparser
import os
from pathlib import Path

def default_conf(platform):
    '''
    This function creates an default configuration
    It takes no parameters but returns a dictionary
    Parameters
    ----------
    platform    : str
                  sys.platform

    Returns
    -------
    config  :   dict
                configuration
    '''
    config = {}
    ###projet
    config['Project_info'] = {}
    config['Project_info']['Name'] = 'New project'
    #config['Project_info']['Project_directory'] ='/home/romain/Documents/STON_data' #Path.home()
    config['Project_info']['Directory'] ='/Users/romainthomas/Documents/STON_data' #Path.home()

    ###tool
    config['Conf'] = {}
    config['Conf']['Window-width'] = 1550
    config['Conf']['Window-height'] = 900
    config['Conf']['OS'] = get_OS(platform)

    ###options
    config['Options'] = {}
    config['Options']['Image_width'] = 100  ###assumed to be squared
    config['Options']['Downgrade_factor'] = 10
    config['Options']['Extensions'] = ['.tif', '.png']

    return config


def load_conf(file, platform):
    '''
    This function loads a configuration file given to the command line interface
    
    Parameter
    ---------
    file	: str
		  configuration file (with path)
    platform    : str
                  sys.platform


    Return
    ------
    config	: dict
                  configuration
    '''

    ###Check that the file exist
    my_file = Path(file)
    if not my_file.is_file():
        return {}, 'no file'

    ##Create empty dictionaty	
    config = {}

    ###create the config object 
    loadconf = configparser.ConfigParser() 

    ###And read the file
    loadconf.read(file)

    ##Extract the conf and organise it
    config['Project_info'] = {}
    config['Project_info']['Name'] = loadconf['Project_info']['Name']
    config['Project_info']['Directory'] = loadconf['Project_info']['Directory']

    ###tool
    config['Conf'] = {}
    config['Conf']['Window-width'] = int(loadconf['Conf']['Window-width'])
    config['Conf']['Window-height'] = int(loadconf['Conf']['Window-height'])
    config['Conf']['OS'] = get_OS(platform)

    ###options
    config['Options'] = {}
    config['Options']['Image_width'] = int(loadconf['Options']['Image_width'])
    config['Options']['Downgrade_factor'] = int(loadconf['Options']['Downgrade_factor'])
    extensions = loadconf['Options']['Extensions'].split(';')
    
    config['Options']['Extensions'] = ['*'+i for i in extensions]

    return config, 'Configuration file found'

def get_OS(platform):
    '''
    SImple function that gets the right OS
    Parameters
    ----------
    None

    Return
    ------
    OS	:	str
                Name of the OS
    '''
    ###general info
    if 'linux' in platform:
        OS = 'Linux'
    elif 'darwin' in platform:
        OS = 'OSX'
    else:
        OS = 'Windows'

    return OS
