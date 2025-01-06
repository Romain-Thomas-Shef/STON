"""
This file is part of the STON project (P.I. E. Dammer)
It loads the configuration of the tool.
if no configuration was given, it will load an empty one
if one was given it will extract configuration from it.

Author: R. Thomas
Place: U. of Sheffield, RSE team
Year: 2024-2025
"""

###Python standard library
import os
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

    ###get the default configuration file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_default = os.path.join(dir_path, 'example.conf')

    ##load it
    config, msg = load_conf(conf_default, platform)    

    ###projet
    config['Project_info']['directory'] = os.path.join(Path.home(), 'Documents')

    ###tool
    config['Conf']['OS'] = get_os(platform)

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

    ##extract the full configuration
    for section in loadconf.sections():
        config[section] = dict(loadconf[section])

    ###Modify extension from str to list
    extensions = loadconf['Project_info']['extensions'].split(';')
    config['Project_info']['extensions'] = ['*'+i for i in extensions]

    ##All elements in the 'Conf' section are ints
    for i in config['Conf']:
        config['Conf'][i] = int(config['Conf'][i])

    ###Add extra elements
    config['Conf']['OS'] = get_os(platform)

    ##All elements in the 'Option' section are ints
    for i in config['General_image_display']:
        config['General_image_display'][i] = int(config['General_image_display'][i])

    ###All elements in the 'Meta' section are ints
    for i in config['Meta_image_options']:
        if i not in ['name_on_images']:
            config['Meta_image_options'][i] = int(config['Meta_image_options'][i])
        else:
            if config['Meta_image_options'][i].lower() == 'yes':
                config['Meta_image_options'][i] = True 
            else:
                config['Meta_image_options'][i] = False

    return config, 'Configuration file found'

def get_os(platform):
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
        op_sys = 'Linux'
    elif 'darwin' in platform:
        op_sys = 'OSX'
    else:
        op_sys = 'Windows'

    return op_sys
