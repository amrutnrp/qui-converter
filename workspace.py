
import xml.etree.ElementTree as ET
import re, os, sys

from get_elements import  get_elements
from process_ui_elements import *

var, _a, b= get_elements('ui/a1.ui')






file_string = custom_ui_translate_iuplua(var)
# file_string_towrite = custom_uip ( a  )
dump_data (file_string, 'result', '.lua', cwd)

#dump_data (c)
print ('Done\n')






