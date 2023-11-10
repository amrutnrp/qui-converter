# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:47:08 2023

@author: amrutnp
"""
import os, re
#  ============  user defined variables   ========================
extra_compact_flag = False
print_missing_kw_flag = False
scale = 1

## ============  designer version specific variables  ============
default_font_size = 8  # in qt designer
default_font_family = 'MS Shell Dlg 2'
default_font_weight = 1


default_font_size = str( int ( default_font_size * scale) ) # varies for each library
cwd = os.getcwd()

def formatError(x):
    input (str(x))
    raise SystemExit

def dump_data( file_str, filename = 'result',ext = '.py', cwd = '.'):
    if '``output' not in os.listdir ( cwd ):
        os.mkdir (cwd + '/``output')
    with open( cwd + '/``output/'+filename+ext, "w", encoding="utf-8") as f:
        f.write(file_str)

class indent_num_class ():
    def __init__(self, libType = 1):
        self.x = 0
        self.mod_Flag = 0
        self.limit_indentation = True if libType == 0 else False                  # in case of pyFLTK, the indentation doesn't have to repeat for all widgets
    def inc(self):                                                               # but in dearpygui, it does
        if self.limit_indentation and self.x ==2 :
            self.mod_Flag += 1
            return
        self.x += 1
    def dec(self):
        if self.mod_Flag > 0 :
            self.mod_Flag -= 1
            return
        self.x -= 1
    def get(self):
        return self.x



def write_indented_function (a, indent_num):
    '''
    this function groups all helper lines into one line
    for example, we declare a item, set the properties, connect the function, trigger another UI
    all of that can be done in one line, it's easy to view
    '''
    global extra_compact_flag
    indent_space =  '    '* indent_num if type(indent_num) == int else '    '* indent_num.get()
    a2= ''
    if extra_compact_flag:
        return indent_space + a
    else:
        for i in a.split(';'):
            a2 += indent_space + i + '\n'
        return a2 [:-1]



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

    master_string = write_indented_function (master_string, indent_num)
    return master_string


    pass




def custom_ui_translate_tk (var):
    template_path = os.path.join (cwd ,'Templates', 'tk_templates' )
    widget_translation  = {
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
        'QComboBox'    :  'Button',
        }
    dismiss_classes_tk = ['QMenuBar', 'QStatusBar']

    def write_gui_template_tk (     list_item = [],
                                    parent = '',
                                    extras= '',
                                    glob_var_zip = []       ):
        if (len(list_item) == 0 or len(glob_var_zip) ==0):
            formatError('WRong argument selection in TK function')

        slate               = ''
        add_later           = ''
        extras_1            = ''
        parent_next         = parent
        indent_var          = 0 if parent== '' else 2
        widget_counter      = glob_var_zip [0]
        for item in list_item:
            if type(item) == dict:                                              # build widget
                if item['name'] == 'centralwidget' or item['class'] in dismiss_classes_tk:
                    continue
                else:
                    if 'pointsize' not in item: item ['pointsize'] = default_font_size             # these items are used in template libraries
                    if 'family' not in item: item ['family'] = default_font_family                 # so initializing these for code safety


                    # if 'weight' not in item: item ['weight'] = default_font_weight               #Don't know
                    # if 'bold' not in item:                                                       # RFU
                    #         item ['bold'] = default_bold_stat                                    #
                    # else:                                                                        #
                    #     if item ['bold'] == 'True':                                              #
                    #         item ['bold'] = 'Bold'                                               #
                    #     else:                                                                    #
                    #         item ['bold'] = ''                                                   #

                    item.update ( { 'eq_name': widget_translation[item ['class']] } )
                    template_file= os.path.join (template_path , item['class'] + '.txt' )
                    parent_next = item['class'] + str(widget_counter)
                    widget_counter += 1
                    if item['class'] == 'QHBoxLayout':
                        extras_1 = 'pack(side = \'left\', expand=True, fill=\'x\')'
                    elif item['class'] == 'QVBoxLayout' :
                        extras_1 = 'pack(side = \'top\', expand=True, fill=\'y\')'

                    if os.path.exists (template_file  ):
                        f2 = open  (template_file, 'r')
                        str_1 = f2.readlines()
                        f2.close()
                        if 'import' in str_1[0]:                                 #most likely Qmainwidget
                            f2 = open  (template_file, 'r')
                            str_2 = f2.read()
                            f2.close()
                            str_3 = str_2.split('{middle}')  #check if it's main
                            if len(str_3) == 1:
                                formatError ('Invalid Template for QMainWidget')
                            add_later = format_template ( str_3 [-1], item , indent_var, True, parent, extras)
                            slate +=  format_template(str_3[0] ,item , indent_var, True, parent, extras)+ '\n'
                        else:
                            str_4 =  format_template (str_1 , item, indent_var, False, parent, extras)
                            slate +=  str_4  + '\n'
                    else:
                        print ('Template not present for : ', item['class'])

            elif type (item) == list:                                             # loop through again
                glob_var_zip = [widget_counter]
                slate += write_gui_template_tk (item, parent_next, extras_1,glob_var_zip  )
                widget_counter = glob_var_zip[0]
            else:
                formatError("unexpected data format")

        slate += add_later
        return slate

                                         # initialize indent variable that'll be tracked throughout the writing of template_file
    file_string = write_gui_template_tk (   var,
                                            parent = '',
                                            extras= '' ,
                                            glob_var_zip = [ 1 ] )
    return file_string



def custom_ui_translate_pyfltk_dpg (var, lib_flag):
    if lib_flag == 0:
        template_path = os.path.join (cwd ,'Templates', 'pyfltk_templates' )
    elif lib_flag == 1:
        template_path = os.path.join (cwd ,'Templates', 'dpg_templates' )
    else:
        formatError ('odd library selected, quitting')


    dismiss_classes = ['QMenuBar', 'QStatusBar']

    def write_gui_template_pyfltk_dpg (     list_item = [],
                                            parent = '',
                                            extras= '',
                                            glob_var_zip = []       ):
        if (len(list_item) == 0 or len(glob_var_zip) ==0):
                formatError('WRong argument selection in TK function')

        slate               = ''
        add_later           = ''
        extras_1            = ''
        parent_next         = parent
        widget_counter      = glob_var_zip [0]
        indent_var          = glob_var_zip [1]

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

                    template_file= os.path.join (template_path , item['class'] + '.txt' )
                    parent_1 = item['class'] + str(widget_counter)
                    widget_counter += 1

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
                            add_later = format_template ( str_3 [-1], item , indent_var, True, parent, extras)
                            slate +=  format_template(str_3[0] ,item , indent_var, True, parent, extras)+ '\n'
                        else:
                            str_4 =  format_template (str_1 , item, indent_var, False, parent, extras)
                            slate +=  str_4  + '\n'
                    else:
                        print ('Template not present for : ', item['class'])

            elif type (item) == list:  # loop through again
                indent_var.inc()
                glob_var_zip = [widget_counter, indent_var]
                slate += write_gui_template_pyfltk_dpg (item, parent_next, extras_1, glob_var_zip)
                widget_counter, indent_var= glob_var_zip [0],  glob_var_zip [1]
                indent_var.dec()
            else:
                formatError("unexpected data format")

        slate += add_later
        return slate

    indent_num = indent_num_class(lib_flag)
    file_string = write_gui_template_pyfltk_dpg (   var,
                                            parent = '',
                                            extras= '' ,
                                            glob_var_zip = [ 1 , indent_num] )
    return file_string


# def custom_ui_translate_iupcpp(var):
    # pass

if __name__ == "__main__":
    from get_elements import get_elements
    a, _a, b= get_elements('ui/app.ui')


    file_string_towrite = custom_ui_translate_tk ( a )
    dump_data (file_string_towrite, 'result', '.py', cwd)

    #dump_data (c)
    print ('Done\n')

'''
for tk, pyfltk, dearpygui
QMainWindow Template file is more than 15 lines long.. im using that in logic
each template must contains keywords inside {} --> that must match with dictionary kws
each line must contain minimum kws - so as not to interfere with other kws
leading and trailing spaces in each line will be removed
'''








