# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:57:15 2023

@author: amrutnp
"""

import xml.etree.ElementTree as ET
import re, os, sys

from get_elements import  get_elements
from process_ui_elements import *

a, _a, b= get_elements('ui/text_base.ui')


def custom_ui_translate_iupcpp(var):
    pass


def custom_uip (var):

    template_path = os.path.join (cwd ,'Templates', 'iupcpp_templates' )
    dismiss_classes = ['QMenuBar', 'QStatusBar']

    def write_gui_template_iup (            list_item = [],
                                            parent = '',
                                            glob_var_zip = [],
                                            yield_children = []
                                            ):
        if (len(list_item) == 0 or len(glob_var_zip) ==0 or len(yield_children) == 0):
                formatError('WRong argument selection in TK function')

        slate               = ''
        add_later           = ''
        parent_next         = parent
        widget_counter      = glob_var_zip [0]

    



        for item in list_item:
            if type(item) == dict:  # build widget
                if item['name'] == 'centralwidget' or item['class'] in dismiss_classes:
                    continue
                else:
                    if 'pointsize' not in item: item ['pointsize'] = default_font_size
                    if 'family' not in item: item ['family'] = default_font_family

                    template_file= os.path.join (template_path , item['class'] + '.txt' )
                    #parent_next = item['class'] + str(widget_counter)
                    widget_counter += 1












        for item in list_item:
            if type(item) == dict:  # build widget
                if item['name'] == 'centralwidget' or item['class'] in dismiss_classes:
                    continue
                else:
                    if 'pointsize' not in item: item ['pointsize'] = default_font_size
                    if 'family' not in item: item ['family'] = default_font_family

                    template_file= os.path.join (template_path , item['class'] + '.txt' )
                    parent_next = item['class'] + str(widget_counter)
                    widget_counter += 1

                    if os.path.exists (template_file  ):
                        f2 = open  (template_file, 'r')  ; str_1 = f2.readlines()  ; f2.close()
                        if '#' in str_1[0]:                   #most likely Qmainwidget
                            f2 = open  (template_file, 'r')
                            str_2 = f2.read()
                            f2.close()
                            str_3 = str_2.split('{middle}')  #check if it's main
                            slate +=  format_template(str_3[0] ,item ,  0, True, parent, extras)+ '\n'
                        else:
                            str_4 =  format_template (str_1 , item,  0, False, parent, extras)
                            slate +=  str_4  + '\n'
                    else:
                        print ('Template not present for : ', item['class'])

            elif type (item) == list:  # loop through again
                glob_var_zip = [widget_counter]
                slate += write_gui_template_iup (item, parent_next, glob_var_zip)
                widget_counter= glob_var_zip [0]
            else:
                formatError("unexpected data format")

        slate += add_later
        return slate






    file_string = write_gui_template_iup (   var,
                                            parent = '',
                                            extras= '' ,
                                            glob_var_zip = [ 1 ] )
    return file_string




















file_string_towrite = custom_uip ( a  )
dump_data (file_string_towrite, 'result', '.py', cwd)

#dump_data (c)
print ('Done\n')







