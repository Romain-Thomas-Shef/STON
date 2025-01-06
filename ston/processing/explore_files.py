"""
This file is part of the STON project (P.I. E. Dammer)
It contains the functions related to file exploration


Author: R. Thomas
Place: U. of Sheffield, RSE team
Year: 2024-2025
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
        _, extension = os.path.splitext(stuff)

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


def get_files_and_path(filelist_selected, original_file_dict, ignorefiles):
    '''
    This function checks creates a list of files (with there path).
    If goes over the filelist_selected list and find where they are
    located in the original_file_dict

    Parameters
    ----------
    filelist_selected   :   list
                            list of file to assemble

    original_file_dict  :   dict
                            original file dictionary
                            keys = absolute path
                            values = filename

    ignorefiles         :   list
                            of files not to add to the final list
    Returns
    -------
    list_with_path      : list
                          of files with their path
    list_without_path   : list
                          list of filenames
    '''
    list_with_path = []
    list_without_path = []

    for name in filelist_selected:
        ##for each entry in the list we check in the dictionary
        for folder in original_file_dict:
            ###first we have to check the name is a folder
            if os.path.basename(folder) != name:
                ##if not we can try to find the file. We also check that it was not already
                ##found in another folder
                for file in original_file_dict[folder]:
                    if file == name and file not in list_without_path and file not in ignorefiles:
                        list_with_path.append(os.path.join(folder,name))
                        list_without_path.append(name)

    return list_with_path, list_without_path
