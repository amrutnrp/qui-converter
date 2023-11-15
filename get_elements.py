# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:57:15 2023

@author: amrutnp
"""

import xml.etree.ElementTree as ET
import re, os, sys

def formatError(x):
    input (str(x))
    SystemExit

def unwrap_tree(tree_1, record ):   # unwraps  only element tree variables
    record.append ( tree_1.tag )
    record.append ( tree_1.attrib )                                               # attrib is always a dictionary
    record.append ( tree_1.text )                                                 # text is always blank for widget trees /  None
    for child_tree in tree_1:
        record.append([])
        unwrap_tree(child_tree, record[-1])


def Process_tree_data( list_item ):
    ''' Returns dictionary variable ; in lookup table format '''

    if len(list_item) < 3:                                                         # length never should be less than 3
        print (' too small item -', list_item)

    if len(list_item) == 3:
        if  list_item[0] == 'widget' and list_item[2] == None:                     # use case 11, a widget with no property of it's own
            return [list_item[1]]
        # if bool( list_item[1]):
        if type( list_item[1]) != dict:                                            # If len==3, the 2nd item must be a dictionary
            print (list_item)
            formatError ('Dict exists in 3 len !!')
        t= {}                                                                      # covers use cases 5,6,7
        t[ list_item[0] ] = list_item [2]
        return t

    if len(list_item[2].strip()) != 0:                                             # for some reason, .text attribute is always blank in qt xml files
        print (list_item)                                                          # use cases with attribute =None is already convered above
        print ( '===',(list_item[2]) )
        formatError ('Non blank string LOL ')

    if not bool( list_item[1]  ):                                                  # it may be rect, font, item,  ... not pointsize
        if list_item[0] == 'item':                                                 # it's just item, bypass the path, cuz it gives a list that can't be processed below
            if len(list_item) != 4:                                                # there must be 4 items , if not , print and ignore it
                print ('Error: other widgets ignored under \'item\' ',list_item)
            return Process_tree_data(list_item[3])
        t={}
        for item in list_item[3:]:                                                 # it's not item !!
            t2= Process_tree_data ( item )
            # print(t,  t2)
            t.update(t2)
        return t

    if list_item[0] == 'property':
        property_name = list_item[1]['name']                                       # property list always follows with a dict with name saying what property it is

        if property_name == 'geometry':
            return Process_tree_data ( list_item[3] )
        elif property_name == 'font':                                              # parent of use case 12
            t2 = Process_tree_data (list_item[3])
            return t2
        elif property_name == 'windowTitle':                                       # use case 13
            t2 = Process_tree_data (list_item[3])
            return {'name' : t2 ['string']}
        elif property_name == 'sizePolicy':                                        # RFU
            pass
        elif property_name == 'windowOpacity':                                     # RFU
            pass
        elif property_name == 'tabShape':                                          # RFU
            pass
        elif property_name == 'enabled':                                           # check for disabled items
            t2 = Process_tree_data (list_item[3])
            return {property_name : t2 ['bool']}
        elif property_name == 'text':                                              # use case 14
            t2 = Process_tree_data (list_item[3])
            return {property_name : t2 ['string']}

    if list_item[0] != 'widget' and list_item[0] != 'layout' :                     # Exclude if it's none of : Widget, Layout and Property
        return {}                                                                  # Also applicable for property that doesn't return anything (RFU)

    t2 =[ list_item[1]]                                                            # now onwards it's only widget / layout
    for i in list_item[3:]:
        t3 = Process_tree_data (i)                                                 # process items individually
        if bool(t3):                                                               # remove blank results
            if type(t3) == dict:
                if list_item[0] == 'layout':
                    print (t3)
                    formatError ('Dictionaries shouldn\'t be present under layout')
                else:
                    t2[0].update (t3)
            if type (t3) == list:
                t2.append (t3 )                                                    # Final item  =[ dict, list --list-- list ]
    if list_item[0] == 'widget' :
        if t2 [0]['class'] == 'QWidget' and 'LayoutWidget' in t2[0]['name']:        # layoutWidget widget is just a container, then simplify it
            if len (t2) == 2:                                                       # first item is always property=geometry, 1nd item is always a QHBOxLayout or something
                t2[0].update(  t2[1][0])                                            # so add the property into top dictinary and keep other widgets in the list
                t2 = [ t2[0] ] + t2[1] [1:]                                         # property is already merged in above section, so it's just 2 items
            else:
                print ('malformed layout widget')
    return t2




def get_elements(file):
    mytree = ET.parse(file)
    root = mytree.getroot()
    if 'version' not in root.attrib:
        print ('invalid UI file')
        SystemExit
    if root.attrib['version'] != '4.0':
        print ('the script was designed for version 4.0 '\
               '\nCurrent Version is {}' \
               '\nmay need to be modified for current verison'.format(root.attrib['version']))
        raise SystemExit()
    '''
    class {} --> contains declaration of Mainwindow, one line only
    widget {'class': 'QMainWindow', 'name': 'MainWindow'}
    tabstops {} --> contains tab order, ignoring for now
    resources {} --> blank for my current examples
    connections {} --> contains signals and slots; to be ignored

    '''
    #=============================================================================================================


    if root[1].tag != 'widget':
        formatError ('bad syntax 1')

    widget_block = root[1]

    #=============================================================================================================
    # Get tab order , store it for future use
    #=============================================================================================================

    tab_order = []
    if root.find('tabstops')== None :
        print ('Tab order not present')
    else:
        tab_order_block = root[2]
        for i in tab_order_block.iter('tabstop'):
            tab_order.append(i.text)

    #=============================================================================================================
    # Unwrap the whole tree, extract all possible data in raw form
    #=============================================================================================================

    all_val=[]

    unwrap_tree(widget_block, all_val)
    # this function takes list and modifies it

    #=============================================================================================================
    # Process the raw data into list and dictinaries  ---- good for visualization
    #=============================================================================================================

    all_val_2 = Process_tree_data( all_val)                                         # removes redundant data and returns compact data in list form


    return all_val_2, tab_order, all_val

if __name__ == "__main__":
    s= get_elements('ui/a.ui')



