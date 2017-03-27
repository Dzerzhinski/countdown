# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 22:59:09 2017

@author: johns
"""

import timerFont as TimerFont 

def get_time_left(ttl_time, now): 
    t_minus = ttl_time - now 
    if(t_minus < 0): 
        t_minus = 0 
    return t_minus

def time_to_str(time): 
    s = time % 60 
    time = time // 60 
    m = time % 60 
    time = time // 60 
    h = time 
    time_str = "{:02d}:{:02d}:{:02d}".format(h, m, s)
    return time_str 
    
def countdown_str(ttl_time, now): 
    t_minus = get_time_left(ttl_time, now) 
    t_minus_str = time_to_str(t_minus) 
    return t_minus_str

def svg_header(font, width, height): 
    
    svg_head = "<?xml version=\"1.0\"?>\n\n" 
    
    svg_head += '<svg '
    svg_head += 'width="{}pt" '.format(str(width)) 
    svg_head += 'height="{}pt" '.format(str(height)) 
    svg_head += 'xmlns="http://www.w3.org/2000/svg">\n\n' 
    
    svg_head += 2 * " " +  "<defs>\n" + \
                4 * " " + "<style type=\"text/css\">\n" + \
                6 * " " + "<![CDATA[\n" + \
                8 * " " + "@font-face {\n" 
    svg_head += 10 * " " + "font-family: '{}';\n".format(font.name) 
    svg_head += 10 * " " + "src: url('{}');\n".format(font.fpath) 
    if (font.tnum): 
        svg_head += 10 * " " + "font-variant-numeric: tabular_nums;\n" 
    svg_head += 8 * " " + "}\n\n" 
    
    svg_head += 8 * " " + "text {\n" 
    svg_head += 10 * " " + "font-size: {}pt;\n".format(font.pt_size) 
    svg_head += 10 * " " + "text-anchor: end;\n" 
    svg_head += 8 * " " + "}\n" 
    svg_head += 6 * " " + "]]>\n" 
    
    svg_head += 4 * " " + "</style>\n" 
    svg_head += 2 * " " + "</defs>\n\n" 
    
    return svg_head 
    
def svg_digit(x, y, digit): 
    digit_str = "    <text x=\"{}pt\" y=\"{}pt\">{}</text>\n".format(x, y, digit) 
    return digit_str 
    
def svg_digit_display(font, hhmmss): 
    x = 0
    display_str = ""
    for i in range(len(hhmmss)): 
        if((i + 1) % 3 == 0): 
            x += font.adv_col 
        else: 
            x += font.adv_dig 
        display_str += svg_digit(x, font.baseline, hhmmss[i]) 
    return display_str 
    
def build_svg(font, hhmmss): 
    height = font.ascent - font.descent + 2 * font.lineGap 
    width = (2 * font.adv_col) + (6 * font.adv_dig)
    svg = svg_header(font, width, height) 
    svg += svg_digit_display(font, hhmmss) 
    svg += "</svg>" 
    return svg 
    
def make_svg_file(font, hhmmss, filename): 
    svg_text = build_svg(font, hhmmss) 
    svgfile = open(filename, "w") 
    svgfile.write(svg_text) 
    svgfile.close() 
    return     