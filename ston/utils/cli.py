"""
This file is part of the STON project (P.I. E. Dammer)
It codes the command line interface


Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2024-2025
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
            '\n - Licence: GPLv3 - '+\
            '\n------------------------------------------------', \
            formatter_class=argparse.RawTextHelpFormatter)

    ###add arguments
    parser.add_argument('--config', help='Configuration file. If no given,'+
                                         '\nSTON will use default configuration',
                                         default='default')
    parser.add_argument('--makeconfig', help='This command will create blank configuration'+\
                                             ' file in the current directory', action='store_true')
    parser.add_argument('--tests', action='store_true', help='Run ston tests')
    parser.add_argument('--version', action='version', version='0.1')

    ###analyse the arguments
    parsed = vars(parser.parse_args(args))

    return parsed
