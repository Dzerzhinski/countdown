# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 15:23:25 2016

@author: john
"""

import re
import subprocess
import os

from fontTools import ttLib as TTLib 

font_name = "monofur" 

def find_font_file(font_name): 
    shell_call_args = ["convert", "-list", "font"] 
    shell_call = subprocess.Popen(shell_call_args, stdout = subprocess.PIPE) 
    font_list = shell_call.communicate()[0].decode(encoding = 'ascii')
    
    fname_exp = re.compile(r"^\s*Font: " + font_name + r"$", re.M)
    fpath_exp = re.compile(r"^\s*glyphs: (.*)$", re.M)
    
    fname_match = fname_exp.search(font_list) 
    fpath_match = fpath_exp.search(font_list, fname_match.start()) 

    if fpath_match is None: 
        return None
    
    return fpath_match.group(1) 
    
print(find_font_file("monofur"))
print(os.path.isfile(find_font_file("monofur")))

font = TTLib.TTFont(file = find_font_file(font_name)) 
