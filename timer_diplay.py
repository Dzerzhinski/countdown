# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 15:23:25 2016

@author: john
"""

import re
import subprocess

from fontTools import ttLib as TTLib 

# font_name = "Times-New-Roman" 
# point_size = 100 

COLON = 0 
DIGIT = 1 
POINTS = 2

CMD = ["magick"]
BG = ["-background", "black"] 
F_COLOR = ["-fill", "white"] 
TXT_POS = ["-gravity", "center"] 
OUTPUT = ["-verbose"] 

def find_font_file(font_name): 
    shell_call_args = ["magick", "-list", "font"] 
    shell_call = subprocess.Popen(shell_call_args, stdout = subprocess.PIPE) 
    font_list = shell_call.communicate()[0].decode(encoding = 'ascii')
#    print(font_list) 
#    print(type(font_list))     
    
    fname_exp = re.compile(r"^\s*Font: " + font_name + r".?$", re.M)
    fpath_exp = re.compile(r"^\s*glyphs: ([^\r]*)\r$", re.M)
    
    fname_match = fname_exp.search(font_list) 
    if(fname_match is None): 
        print("Fuck") 
    fpath_match = fpath_exp.search(font_list, fname_match.start()) 

    if fpath_match is None: 
        return None
    
    return fpath_match.group(1) 
    
def find_metrics(font_name, point_size): 
    # find font
    font = TTLib.TTFont(file = find_font_file(font_name)) 

    # get unicode map
    umap = None 
    for t in font["cmap"].tables: 
        if t.isUnicode(): 
            umap = t 
            break 
    # get maximum integer digit advance
    amax = 0
    for i in range(10): 
        gname = umap.cmap[ord(str(i))] 
        advance = font["hmtx"].metrics[gname][0]
        if(advance > amax): 
            amax = advance
    # get colon glyyph advance
    colon_advance = font["hmtx"].metrics[umap.cmap[ord(":")]][0] 
    # get font em
    em = font["head"].unitsPerEm 

    dig_size = (int(point_size * amax / em))
    col_size = (int(point_size * colon_advance / em)) 

    
    return col_size, dig_size 

def make_file(lab, font_name, width, point, fname): 
    # prepare arguments
    font_arg = ["-font", font_name] 
    size_arg = ["-size", str(width) + "x" + str(point)] 
    points_arg = ["-pointsize", str(point)] 
    label_arg = "label:" + lab
    arg_list = CMD +  font_arg + BG + F_COLOR + TXT_POS + OUTPUT +\
                size_arg + points_arg
    arg_list.extend([label_arg, fname]) 
    print("ping")
    print(" ".join(arg_list))
            
    shell_call = subprocess.Popen(arg_list, stdout = subprocess.PIPE) 
    print(shell_call.communicate()[0].decode(encoding = 'ascii'))

def make_countdown_img(font_name, size_list, hhmmss): 
            
    timer_display = [":", str(hhmmss[0]).zfill(2), str(hhmmss[1]).zfill(2),\
                    str(hhmmss[2]).zfill(2)]                
                    
    file_col = "C:/Users/johns/temp_col.gif"
    file_dig = ["C:/Users/johns/temp_hh.gif",\
                "C:/Users/johns/temp_mm.gif",\
                "C:/Users/johns/temp_ss.gif"]
    file_out = "C:/Users/johns/temp.gif"
    
    
    make_file(timer_display[0], font_name, size_list[COLON],\
                size_list[POINTS], file_col) 
    for i in range(1, 4) :
        make_file(timer_display[i], font_name, size_list[DIGIT] * 2, size_list[POINTS],\
                    file_dig[i - 1]) 
    
    
    shell_call_4 = subprocess.Popen(["montage", "-geometry", "+0",\
                                        "-tile", "x1",\
                            file_dig[0], file_col, file_dig[1],\
                            file_col, file_dig[2], file_out],\
                            stdout = subprocess.PIPE) 
    print(shell_call_4.communicate()[0].decode(encoding = "ascii"))
    return file_out

    