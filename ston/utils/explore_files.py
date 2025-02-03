"""
This file is part of the STON project (P.I. E. Dammer)
It contains the functions related to file exploration


Author: R. Thomas
Place: U. of Sheffield, RSE team
Year: 2024-2025
"""

####Standard Library
import os
import glob
from collections import Counter

##Third party

##local imports

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
    files_dict    :   dictionary
                      with key=directory
                           value=list of files in that directory
    '''

    file_dict = {}
    all_files = []

    ##Remove stars from extension
    extensions = [i.lstrip('*') for i in extensions]

    ##Get all files, recusrively
    for ext in extensions:
        all_files_for_that_extension = glob.glob(os.path.join(root, f'**/*{ext}'), 
                                                 recursive=True)
        
        all_files += all_files_for_that_extension 

    ##Extract directory names
    all_dir = []
    for file in all_files:
        all_dir.append(os.path.dirname(file))

    ###Using Counter with are counting the number of time each directory
    ###Appears. We don't care about the number but just the list of
    ###directories. With them we create the entries in the final dictionary
    for directory in Counter(all_dir):
        file_dict[directory] = []

    ###And fill up the dictionary
    for file in all_files:
        for directory in file_dict:
            if os.path.dirname(file) == directory:
                file_dict[directory].append(os.path.basename(file))
                
    return file_dict


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
