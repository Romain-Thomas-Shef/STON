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

    ###get the default configuration file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_default = os.path.join(dir_path, 'example.conf')

    ##load it
    config, msg = load_conf(conf_default)
    del msg

    ###project
    config['Project_info']['directory'] = os.path.join(Path.home(), 'Documents')

    return config

def test_conf():
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

    ###get the default configuration file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_default = os.path.join(os.path.dirname(dir_path), 'test_data/test.conf')
    
    ##load it
    config, msg = load_conf(conf_default)
    del msg

    ###project
    config['Project_info']['directory'] = os.path.dirname(dir_path)

    return config



def load_conf(file):
    '''
    This function loads a configuration file given to the command line interface
    
    Parameter
    ---------
    file	: str
		  configuration file (with path)

    Return
    ------
    config	: dict
                  configuration
    '''

    ###Check that the file exist
    my_file = Path(file)
    if not my_file.is_file():
        return {}, 'no file'

    ##Create empty dictionary
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

    ##zoom
    config['Zoom_window']['closeup_window_size'] = \
                int(config['Zoom_window']['closeup_window_size'])

    ##All elements in the 'Conf' section are ints
    for i in config['Conf']:
        config['Conf'][i] = int(config['Conf'][i])

    ##All elements in the 'Analysis' section are float
    for i in config['Analysis']:
        config['Analysis'][i] = float(config['Analysis'][i])

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
