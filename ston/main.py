"""
This file is part of the STON project (P.I. E. Dammer)
It is where the application starts.

Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
version: 0.1

changelog:
----------
0.1 : RTh - Creation of the file
"""

####Standard Library
import os
import shutil
import sys

####Python third party
from PySide6.QtWidgets import QApplication, QMessageBox

####Local imports
from .cli import command_line_interface
from . import conf
from . import main_window

def main():
    '''
    This is the main function
    '''

    ##1st we use the command line interface to look at potential
    ##arguments
    args = command_line_interface(sys.argv[1:])


    if args['makeconfig']:
        ##get current working directory and create the final path
        targetfile = os.path.join(os.getcwd(), 'STON.conf')
        ###build the path of the template file
        template = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'example.conf')

        ##Make the copy
        shutil.copyfile(template, targetfile)

        sys.exit()

    if args['config'] == 'default': ##no argument passed
        ##In that case we load the default
        configuration = conf.default_conf(sys.platform)
    else:
        ##in that case we extract the configuration from the file
        configuration, msg = conf.load_conf(args['config'], sys.platform)
        if msg == 'no file':
            print(f'Configuration file does not exist. {args["config"]}')
            sys.exit()

    ##create the app
    app = QApplication(sys.argv)
    ex = main_window.GUI(configuration)
    sys.exit(app.exec())
