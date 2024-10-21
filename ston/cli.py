"""
This file is part of the STON project (P.I. E. Dammer)
It codes the command line interface


[change what's below]
Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
version: 0.1

changelog:
----------
0.1: RTh - Creation
"""

###Python standard library
import argparse



def command_line_interface(args):
    '''
    This function defines the command line interface of the program.

    Parameters
    -----------
    args    :   sys.argv
                arguments passed to the interface

    Returns
    -------
    parsed  :   Namespace
                parsed arguments
    '''
    ##create parser object
    parser = argparse.ArgumentParser(description=\
            '------------------------------------------------'+\
            '\n - STON: SofTware for petrOgraphic visualisatioN'+\
            '\n - Authors: R. Thomas & E. Dammer'+\
            '\n - Licence: MIT - '+\
            '\n------------------------------------------------', \
            formatter_class=argparse.RawTextHelpFormatter)

    ###add arguments
    parser.add_argument('--config', help='Configuration file. If no given,'+
                                         '\nSTON will use default configuration',
                                         default='default')
    parser.add_argument('--makeconfig', help='This command will create blank configuration'+\
                                             ' file in the current directory', action='store_true')
    parser.add_argument('--version', action='store_true', help='Prints the version of STON')

    ###analyse the arguments
    parsed = vars(parser.parse_args(args))

    return parsed
