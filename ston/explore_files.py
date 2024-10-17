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

def get_dir_and_files(root, extensions):
    '''
    This function gets all the files and sub directories
    from a root path given in argument

    Warning: it is assumed that the root path exists (it is checked before)

    Parameters
    ----------
    root  : str
            root path
    extensions  : list
                  of possible files extensions

    return
    ------
    tree    :   nested dictionary
                hierarchical tree of files and directories
    '''
   
    tree = {}
    files_only = []

    ##Remove stars from extension
    extensions = [i.lstrip('*') for i in extensions]
 
    for stuff in os.listdir(root):
        ##extract name extension
        filename, extension = os.path.splitext(stuff)

        ###check if it is a file
        if os.path.isfile(os.path.join(root, stuff)) and extension in extensions:
            files_only.append(stuff) 

        ###check if it is a directory
        if os.path.isdir(os.path.join(root, stuff)):
            ##if it is we call the current function on that dictionary
            dictionary = get_dir_and_files(os.path.join(root, stuff), extensions)
            if dictionary:
                tree[list(dictionary.keys())[0]] = dictionary[list(dictionary.keys())[0]]

    ###add to dictionary
    if files_only:
        tree[root] = files_only
    
    return tree

