"""
This file is part of the STON project (P.I. E. Dammer)
It contains the functions related to file exploration


Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
version: 0.1

changelog:
----------
0.1 : RTh - Creation
"""

####Standard Library
import os

def get_dir_and_files(root, with_hidden=False):
    '''
    This function gets all the files and sub directories
    from a root path given in argument

    Warning: it is assumed that the root path exists (it is checked before)

    Parameters
    ----------
    root  : str
            root path
    with_hidden : Bool
                  False (default) if you ignore hidden files
                  True if they must be used

    return
    ------
    tree    :   nested dictionary
                hierarchical tree of files and directories
    '''
    
    tree = {}
    files_only = []
    for stuff in os.listdir(root):
        ###check if it is a file
        if os.path.isfile(os.path.join(root, stuff)):
            if with_hidden:
                files_only.append(stuff) 
            else:
                ##check if the file is hidden
                pass

        ###check if it is a directory
        if os.path.isdir(os.path.join(root, stuff)):
            if with_hidden:
                print(stuff)

    print(files_only)
