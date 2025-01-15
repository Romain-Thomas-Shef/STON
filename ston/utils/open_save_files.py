"""
This file is part of the STON project (P.I. E. Dammer)
It open and saves files

Author: R. Thomas
Place: U. of Sheffield
Year: 2024-2025
"""
###Python standard library

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
    
    '''
    with open(file, 'w', encoding="utf-8") as filetosave:
        filetosave.write(txt)

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

    with open(file, 'r', encoding="utf-8") as filetoread:
        txt = filetoread.read()

    return txt
