"""
This file is part of the STON project (P.I. E. Dammer)
It open and saves files

Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
"""
###Python standard library
import os

##Third party

##Local imports

def save_txt_to_file(file, txt):
    '''
    This function open the file given in argument
    and write the txt given as well
    Parameters
    ----------
    file        :   str
                    path/to/file
    
    txt         :   str
                    text to save
    
    Return
    ------
    status      :  str
                   message
    '''
    if txt:
        if os.path.isdir(os.path.dirname(file)):
            with open(file, 'w', encoding="utf-8") as filetosave:
                filetosave.write(txt)
            status = f'File {file} was saved on disk' 
            print(os.listdir())

        else:
            status = f'Directory {os.path.dirname(file)} does not exist'+\
                      '...File not saved'

    else:
        status = 'No text was passed....we did not save a file'

    return status

def open_txt_file(file):
    '''
    This function open the file given in argument
    and read it line by line
    
    Parameters
    ----------
    file    :   str
                path/to.file to read
    
    Return
    ------
    txt     :   str 
                text from file
    '''

    if os.path.isfile(file):    
        with open(file, 'r', encoding="utf-8") as filetoread:
            txt = filetoread.read()

    else:
        txt = 'The file was not found'

    return txt
