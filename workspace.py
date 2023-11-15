# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:57:15 2023

@author: amrutnp
"""

import xml.etree.ElementTree as ET
import re, os, sys

from get_elements import  get_elements
from process_ui_elements import *

var, _a, b= get_elements('ui/a.ui')


def custom_ui_translate_iupcpp(var):
    pass


def format_template_iupcpp (list_of_strings, dictionary, returnLine_w_noKeyword = False ):
    master_string = ''
    if type(list_of_strings) == str:
        list_of_strings = list_of_strings.split('\n')
        str_addition= '\n'
    else:
        str_addition = ''
    for line in list_of_strings:
        if '{' in line:
            string = line
            kws = re.findall(r'\{.*?\}', line)
            for kw in kws:
                kw2 = kw[1:-1]  # removing the brackets
                if kw2 in dictionary:
                    string = string.replace( kw,  dictionary [kw2] if bool(dictionary [kw2]) else '' )
                # else:
                #     if returnLine_w_noKeyword == True:
                #         string = ''
                #     if print_missing_kw_flag: print ('kw not found :',kw2, dictionary['name'])
        else:
            string = line
        master_string +=  string + str_addition

    return master_string



template_path = os.path.join (cwd ,'Templates', 'iupcpp_templates' )
dismiss_classes = ['QMenuBar', 'QStatusBar']
default_font_str = 'MS Shell Dlg 2 , 8'

def write_gui_template_iup ( list_item = [],  yield_children = []  ):
    if (len(list_item) == 0 or len(yield_children) == 0):
            formatError('WRong argument selection in TK function')

    slate               = ''
    list_of_all_children = []
    current_widget_name = ''


    children_list = []
    for item in reversed(list_item):
        if type (item) == list:  # loop through children first
            ret = write_gui_template_iup (item, yield_children)
            str_slate, child_name = ret[0], ret[1]
            slate += str_slate + '\n'
            list_of_all_children.append (child_name)
            # print (list_of_all_children)

        elif type(item) == dict:  # build widget
            if 'pointsize' not in item or 'family' not in item:                # set a default font
                item ['font_str'] = default_font_str
            else:
                item ['font_str'] = item ['family']+','+ item['pointsize']

            template_file= os.path.join (template_path , item['class'] + '.txt' )
            if os.path.exists (template_file  ):
                f2 = open  (template_file, 'r')  ; str_1 = f2.readlines()  ; f2.close()
                current_widget_name  = item ['name']
                yield_children[0] = yield_children[0]  + list_of_all_children
                item['children'] = ','.join([ i for i in list_of_all_children if i in yield_children [3]])
                # if the children hasn't been defined, then don't include it

                str_4 =  format_template_iupcpp (str_1 , item )
                slate +=  str_4

                if len((''.join(str_1)).strip()) != 0:                         # if the definition is proper, add it to defined list
                    yield_children [3][current_widget_name] = True


            else:
                print ('Template not present for : ', item['class'])
        else:
            formatError("unexpected data format")

    return [ slate, current_widget_name ,list_of_all_children ]



children_list = []
children_data= ['']
immediate_children = []
widget_declaration_status = {}
yield_children = [ children_list , children_data, immediate_children, widget_declaration_status]

main_template = os.path.join (template_path , 'QMainWindow.txt' )
f2 = open  (main_template, 'r')  ; str_1 = f2.readlines()  ; f2.close(); str_1 = ''.join (str_1)
str_blocks = str_1.split('{--}')
file_string = str_blocks [0] +  str_blocks [1]                             # include and main block

ret = write_gui_template_iup (   var [1:], yield_children )
slate2, _a , main_children = ret[0], ret[1], ret[2]


children_list  = yield_children[0]

file_string += '\nIhandle'                                                # the Ihandle declaration block
for i in children_list + main_children:
    file_string += '  *'+i+','
else:
    file_string  = file_string [:-1] + ';'


file_string +=  str_blocks [2]
file_string+= slate2                                                      # widget description block
file_string +=  str_blocks [3]
for i in ret[2]:                                                          #children of main / top level
    if i in widget_declaration_status:
        file_string+= i+','

var[0]['height'] = str( int ( int (var[0]['height'] )+ 40) )              # add something exxtra for top bar
ret2= format_template_iupcpp (str_blocks[4], var[0] , returnLine_w_noKeyword= 'True')

file_string+= ret2
file_string += str_blocks[5]





aaaas = file_string




# file_string_towrite = custom_uip ( a  )
dump_data (file_string, 'result', '.c', cwd)

#dump_data (c)
print ('Done\n')







