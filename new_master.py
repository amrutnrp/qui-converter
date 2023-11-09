# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:48:45 2023

@author: amrutnp
"""

import re, os, sys

from get_elements import  get_elements


args = sys.argv
l= len (args)
if l ==1:
    folder = 'ui\\'
    #====================================

    list_of_files = os.listdir(folder)
    print ('Files Present       ========================>')
    for idx, i in enumerate (list_of_files):                # show the list of files
        print ('\t\t',idx,'\t',i )                          #
    h= input ('Enter a number and Select the file:\t ')
    if not h.isdigit():                                     # check input type
        input ('Wrong file selection input!!')              #
        raise SystemExit()
    else:
        h= int (h)                                          #
    if h>=len(list_of_files):                               # check input in range or not
        input ('Wrong file selection input!!')
        raise SystemExit()
    file = folder + list_of_files [h]                       # get the file path

    #====================================
    h= input ('''
Library Options -- ========================>
        1:      Tkinter
        2:      Dear PyGUI
        3:      py-FLTK
        4:      IUP c++
Enter option for target library:\t''')
    if not h.isdigit():
        input ('Wrong  input!!')
        raise SystemExit()
    else:
        h= int (h)
    if h == 1:
        cvt_lib = 'tk'
    elif h == 2:
        cvt_lib = 'dpg'
    elif h == 3:
        cvt_lib = 'pyfltk'
    elif h == 4:
        cvt_lib = 'iupcpp'
    else:
        input ('Wrong input!!')
        raise SystemExit()
    #====================================
else:
    args = sys.argv
    l= len (args)
    cvt_lib = args[1]
    file = args[2]
    # print (cvt_lib, file)
    # print ('all ok')
    #raise SystemExit()
print ('input all ok\n====================================\n')



all_items, _a, _b = get_elements (file)


