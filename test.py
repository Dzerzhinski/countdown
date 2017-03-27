# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 15:23:25 2016

@author: john
"""

import re
import subprocess

from fontTools import ttLib as TTLib 

font_name = "Times-New-Roman" 
point_size = 100 

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
    
def find_metrics(font): 
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
    
    return em, amax, colon_advance 

def make_file(lab, size, fname): 
    font_arg = ["-font", font_name] 
    size_arg = ["-size", size] 
    points_arg = ["-pointsize", str(point_size)] 
    label_arg = "label:" + lab
    arg_list = CMD +  font_arg + BG + F_COLOR + TXT_POS + OUTPUT +\
                size_arg + points_arg
    arg_list.extend([label_arg, fname]) 
    print("ping")
    print(" ".join(arg_list))
            
    shell_call = subprocess.Popen(arg_list, stdout = subprocess.PIPE) 
    print(shell_call.communicate()[0].decode(encoding = 'ascii'))

def make_countdown_img(font_name, point_size, hhmmss): 
    # find font
    font = TTLib.TTFont(file = find_font_file(font_name)) 
        
    em, dig_adv, col_adv = find_metrics(font) 
    dig_size = str(int(point_size * 2 * dig_adv / em)) + "x" + str(point_size)  
    col_size = str(int(point_size * 2 * col_adv / em)) + "x" + str(point_size)  
    
    hh = 00 
    mm = 22 
    ss = 11 
    
    timer_display = [":", str(hhmmss[0]).zfill(2), str(hhmmss[1]).zfill(2),\
                    str(hhmmss[2]).zfill(2)]                
                    
    lab1 = "label:22"
    lab2 = "label::" 
    lab3 = "label:11"
    file_col = "C:/Users/johns/temp_col.gif"
    file_dig = ["C:/Users/johns/temp_hh.gif",\
                "C:/Users/johns/temp_mm.gif",\
                "C:/Users/johns/temp_ss.gif"]
    file_out = file_col = "C:/Users/johns/temp.gif"
    
    
    make_file(timer_display[0], col_size, file_col) 
    for i in range(1, 4) :
        make_file(timer_display[i], dig_size, file_dig[i - 1]) 
    
    
    shell_call_4 = subprocess.Popen(["montage", "-geometry", "+0",\
                                        "-tile", "x1",\
                            file_dig[0], file_col, file_dig[1],\
                            file_col, file_dig[2], file_out])
