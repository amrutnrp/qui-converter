# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:57:15 2023

@author: amrutnp
"""

import xml.etree.ElementTree as ET
import re, os


folder = 'ui-examples\\'
# file = 'Ver_2.ui'
file = 'fakePromira.ui'
# file = 'new_1.ui'
# file = 'PSI_v1.ui'
# file= 'x.ui'

cvt_lib = 'tk'
# cvt_lib = 'pyfltk'
# cvt_lib = 'dpg'
print_missing_kw_flag = False
extra_compact_flag = False

default_font_size = 8  # in qt designer
default_font_family = 'MS Shell Dlg 2'
default_font_weight = 1

#=============================================================================================================
template_path = cvt_lib+ '_templates' + '\\'


is_fltk = True if cvt_lib.lower() == "pyfltk" else False
is_tk = True if cvt_lib.lower() == "tk" else False

widget_translation  = {
    'tk' :  {
                'QPushButton'  : 'Button',
                'QLabel'       : 'Label',
                'QCheckBox'    :  'Checkbutton',
                'QHBoxLayout'  :  '',
                'QLineEdit'    :  'Entry',
                'QMainWindow'  :  '',
                'QRadioButton' :  'Radiobutton',
                'QTextEdit'    :  '',
                'QVBoxLayout'  :  '',
                'QWidget'      :  '',
                'QTextBrowser' :  '',

            }

    }

scale = 1

default_font_size = str( int ( default_font_size * scale) )

class indent_num_class ():
    def __init__(self):
        self.x = 0
        self.mod_Flag = 0
    def inc(self):
        if (is_tk or is_fltk)and self.x ==2 : self.mod_Flag += 1 ; return
        self.x += 1
    def dec(self):
        if self.mod_Flag > 0 : self.mod_Flag -= 1; return
        self.x -= 1
    def get(self):
        return self.x

mytree = ET.parse(folder+file)
root = mytree.getroot()
if 'version' not in root.attrib:
    print ('invalid UI file')
    SystemExit
if root.attrib['version'] != '4.0':
    print ('the script was designed for version 4.0 '\
           '\nCurrent Version is {}' \
           '\nmay need to be modified for current verison'.format(root.attrib['version']))
'''
class {} --> contains declaration of Mainwindow, one line only
widget {'class': 'QMainWindow', 'name': 'MainWindow'}
tabstops {} --> contains tab order, ignoring for now
resources {} --> blank for my current examples
connections {} --> contains signals and slots; to be ignored

'''
#=============================================================================================================
def formatError(x):
    input (str(x))
    SystemExit

if root[1].tag != 'widget':
    formatError ('bad syntax 1')



widget_block = root[1]

#=============================================================================================================

tab_order = []
if root.find('tabstops')== None :
    print ('Tab order not present')
else:
    tab_order_block = root[2]
    for i in tab_order_block.iter('tabstop'):
        tab_order.append(i.text)

#=============================================================================================================


all_val=[]

def c(tree_1, record ):
    global count
    record.append ( tree_1.tag )
    record.append ( tree_1.attrib )
    record.append ( tree_1.text )
    for i in tree_1:
        record.append([])
        c(i, record[-1])
c(widget_block, all_val)

#=============================================================================================================
# Converted to list and dictinaries  ---- good for visualization
#=========================


def c2( list_item ):
    ''' Returns dictionary   containing values like lookup table '''

    if len(list_item) == 3:
        if  list_item[0] == 'widget' and list_item[2] == None:
            return [list_item[1]]
        if bool( list_item[1]  )  :
            print (list_item)
            formatError ('Dict exists in 3 len !!')
        t= {}
        t[ list_item[0] ] = list_item [2]
        return t
    if len(list_item) < 3:
        print (' too small item -', list_item)
    if len(list_item[2].strip()) != 0:
        print (list_item)
        print ( '===',(list_item[2]) )
        formatError ('Non blank string LOL ')
    if not bool( list_item[1]  ):
        # print('blank 2nd items:  ', list_item[0] ) #must be rect, also item, also font
        if list_item[0] == 'item':
            if len(list_item) != 4:
                print ('Error: other widgets ignored under \'item\' ',list_item)
            return c2(list_item[3])
        t={}
        for item in list_item[3:]:
            t2= c2 ( item )
            # print(t,  t2)
            t.update(t2)
        return t

    if list_item[0] == 'property':
        property_name = list_item[1]['name']

        if property_name == 'geometry':
            return c2( list_item[3] )
        elif property_name == 'font':
            t2 = c2 (list_item[3])
            if 'pointsize' in t2:
                t2['pointsize'] =  str (   int( int ( t2['pointsize'] )* scale ))
            return t2
        elif property_name == 'windowTitle':
            t2 = c2 (list_item[3])
            return {'name' : t2 ['string']}
        elif property_name == 'sizePolicy':
            pass
        elif property_name == 'windowOpacity':
            pass
        elif property_name == 'tabShape':
            pass
        elif property_name == 'enabled':
            t2 = c2 (list_item[3])
            return {property_name : t2 ['bool']}
        elif property_name == 'text':
            t2 = c2 (list_item[3])
            return {property_name : t2 ['string']}

    if list_item[0] != 'widget' and list_item[0] != 'layout' :
        return {}

    # print ('widget discovered')
    #==== now onwards it's only widget
    t2 =[ list_item[1]]
    for i in list_item[3:]:
        t3 = c2(i)
        if bool(t3):
            # print (t2, t3)
            if type(t3) == dict:
                if list_item[0] == 'layout':
                    print (t3)
                    formatError ('Dictionaries shouldn\'t be present under layout')
                else:
                    t2[0].update (t3)

            if type (t3) == list:
                t2.append (t3 )
    if list_item[0] == 'widget' :
        if t2 [0]['class'] == 'QWidget' and 'layoutWidget' in t2[0]['name']:
            if len (t2) == 2:
                t2[0].update(  t2[1][0])
                t2 = [ t2[0] ] + t2[1] [1:]
            else:
                print ('malformed layout widget')
    return t2

all_val_2 = c2( all_val)


# del widget_block, tab_order_block, root, mytree, i, folder, file

#=============================================================================================================


def remove_last_comma (a, indent_num): # it doesn't serve the purpose of removing comma any more- more like processing the text
    global extra_compact_flag
    indent_space =  '    '* indent_num.get()
    a2= ''
    if extra_compact_flag:
        return indent_space + a
    else:
        for i in a.split(';'):
            a2 += indent_space + i + '\n'

        return a2 [:-1]
    #return ''.join(a.rsplit(',',1))  #remove last comma  -- not required anymore

def format_template (list_of_strings, dictionary, indent_num , include_non_kw_lines = False, parent = '', extras = ''):
    master_string = ''
    dictionary.update( { 'parent' : parent })
    if type(list_of_strings) == str:
        list_of_strings = list_of_strings.split('\n')
    for line in list_of_strings:
        if '{' in line:
            string = line
            kws = re.findall(r'\{.*?\}', line)
            for kw in kws:
                kw2 = kw[1:-1]  # removing the brackets
                if kw2 not in dictionary:
                    if kw2 == 'extras' and bool(extras):
                        string = string.replace( kw,  extras )
                    else:
                        if not include_non_kw_lines:
                            string = ''
                        if print_missing_kw_flag: print ('kw not found :',kw2, dictionary['name'])
                else:
                    string = string.replace( kw,  dictionary [kw2] if bool(dictionary [kw2]) else '' )
        else:
            string = line
        master_string +=  string+'\n' if include_non_kw_lines  else string .strip()

    master_string = remove_last_comma (master_string, indent_num)
    return master_string


    pass
no_of_indents = indent_num_class()

dismiss_classes = ['QMenuBar', 'QStatusBar']

parent_1 = ''

def write_gui_template (list_item, parent = '', extras= ''):
    global no_of_indents, counter
    slate = ''
    add_later = ''
    parent_1 = parent
    extras_1= ''
    for item in list_item:
        if type(item) == dict:  # build widget
            if item['name'] == 'centralwidget' or item['class'] in dismiss_classes:
                continue
            else:
                if 'pointsize' not in item: item ['pointsize'] = default_font_size
                if 'family' not in item: item ['family'] = default_font_family
                # if 'weight' not in item: item ['weight'] = default_font_weight
                # if 'bold' not in item:
                #         item ['bold'] = default_bold_stat
                # else:
                #     if item ['bold'] == 'True':
                #         item ['bold'] = 'Bold'
                #     else:
                #         item ['bold'] = ''

                if is_tk: item.update ( { 'eq_name': widget_translation [cvt_lib][item ['class']] } )
                template_file= template_path + item['class'] +'.txt'
                parent_1 = item['class'] + str(counter) 
                counter += 1
                if is_tk:
                    if item['class'] == 'QHBoxLayout':
                        extras_1 = 'pack(side = \'left\', expand=True, fill=\'x\')'
                    elif item['class'] == 'QVBoxLayout' :
                        extras_1 = 'pack(side = \'top\', expand=True, fill=\'y\')'

                if os.path.exists (template_file  ):
                    f2 = open  (template_file, 'r')
                    str_1 = f2.readlines()
                    f2.close()
                    if 'import' in str_1[0]:                   #most likely Qmainwidget
                        f2 = open  (template_file, 'r')
                        str_2 = f2.read()
                        f2.close()
                        str_3 = str_2.split('{middle}')  #check if it's main
                        if len(str_3) == 1:
                            formatError ('Invalid Template for QMainWidget')
                        add_later = format_template ( str_3 [-1], item , no_of_indents, True, parent, extras)
                        slate +=  format_template(str_3[0] ,item , no_of_indents, True, parent, extras)+ '\n'
                    else:
                        str_4 =  format_template (str_1 , item, no_of_indents, False, parent, extras)
                        slate +=  str_4  + '\n'
                else:
                    print ('Template not present for : ', item['class'])

        if type (item) == list:  # loop through again

            no_of_indents.inc()
            slate += write_gui_template (item, parent_1, extras_1)
            no_of_indents.dec()

    slate += add_later
    return slate
'''
QMainWindow Template file is more than 15 lines long.. im using that in logic
each template must contains keywords inside {} --> that must match with dictionary kws
each line must contain minimum kws - so as not to interfere with other kws
leading and trailing spaces in each line will be removed

'''

counter = 1

file_string = write_gui_template ( all_val_2)


with open('result.py', "w", encoding="utf-8") as f:
    f.write(file_string)


if bool(tab_order):
    tab_order_str = '\n\'\'\'\n====Widget_list =====\n\n'
    for item in tab_order:
        tab_order_str += item +'\n'
    tab_order_str +='\'\'\'\n'
    with open('result.py', "a", encoding="utf-8") as f:
        f.write(tab_order_str)























