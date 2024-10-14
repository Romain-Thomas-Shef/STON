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

def default_conf():
    '''
    This function creates an default configuration
    It takes no parameters but returns a dictionary
    Parameters
    ----------
    None

    Returns
    -------
    config  :   dict
                configuration
    '''
    config = {}
    ###projet
    config['Project_name'] = 'New project'


    ###tool
    config['Window-width'] = 1150
    config['Window-height'] = 700

    return config
