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
    config['Project_name'] = 'New project'
    #config['Project_directory'] ='/home/romain/Documents/STON_data' #Path.home()
    config['Project_directory'] ='/Users/romainthomas/Documents/STON_data' #Path.home()

    ###tool
    config['Window-width'] = 1150
    config['Window-height'] = 700

    ###options
    config['Display_area'] = '10x5'
    config['Image_width'] = 200  ###assumed to be squared
    config['Extensions'] = ['.tif', '.png']

    ###general info
    if 'linux' in platform:
        config['OS'] = 'Linux'
    elif 'darwin' in platform:
        config['OS'] = 'OSX'
    else:
        config['OS'] = 'Windows'
        
    return config
