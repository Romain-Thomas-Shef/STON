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
import sys

####Python third party
from PyQt6.QtWidgets import QApplication, QMessageBox

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

    if args['config'] == 'default': ##no argument passed
        ##In that case we load the default
        configuration = conf.default_conf(sys.platform)
    else:
        ##in that case we extract the configuration from the file
        ##configuration = conf.load_conf(args['config'])
        pass

    ##create the app
    app = QApplication(sys.argv)
    ex = main_window.GUI(configuration)
    sys.exit(app.exec())
