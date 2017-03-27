# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 22:59:09 2017

@author: johns
"""

import timerFont as TimerFont 
import subprocess 

#############################################################################
# 
# Convert time passed (t-plus) to time left (t-minus).  (Time in seconds.) 
# 
# @param ttl_time Total time on countdown 
# @param now Time passed (t-plus) 
# @return Time remaining (t-minus) 
# 
#############################################################################
def get_time_left(ttl_time, now): 
    t_minus = ttl_time - now 
    if(t_minus < 0): 
        t_minus = 0 
    return t_minus

############################################################################
# 
# Convert time (in seconds) to string for display in format HH:MM:SS. 
# 
# @param time Time in seconds 
# @return Time in string representation 
# 
#############################################################################
def time_to_str(time): 
    s = time % 60 
    time = time // 60 
    m = time % 60 
    time = time // 60 
    h = time 
    time_str = "{:02d}:{:02d}:{:02d}".format(h, m, s)
    return time_str 
    
############################################################################
# 
# Convert time passed (in seconds) to string representation of time 
# remaining (t-minus).  
# 
# @param ttl_time Total time in countdown 
# @param now Time passed (t-plus) in seconds 
# @return Time remaining (t-minus) in string representation 
# 
############################################################################
def countdown_str(ttl_time, now): 
    t_minus = get_time_left(ttl_time, now) 
    t_minus_str = time_to_str(t_minus) 
    return t_minus_str


#############################################################################
# 
# Helper function to build beginning of svg file.  Includes size and style 
# info.  Uses SVG 2.0 spec since Inkscape supports it.
# 
# @param font TimerFont object 
# @param width Full width of timer display 
# @param height Full height of timer display 
# @return String containing header for SVG file
#
#############################################################################
def svg_header(font, width, height): 
    
    svg_head = "<?xml version=\"1.0\"?>\n\n" 
    
    svg_head += '<svg '
    svg_head += 'width="{}pt" '.format(str(width)) 
    svg_head += 'height="{}pt" '.format(str(height))
    svg_head += 'xmlns="http://www.w3.org/2000/svg">\n\n' 
    
    # Old attempt
#    svg_head += 2 * " " +  "<defs>\n" + \
#                4 * " " + "<style type=\"text/css\">\n" + \
#                6 * " " + "<![CDATA[\n" + \
#                8 * " " + "@font-face {\n" 
#    svg_head += 10 * " " + "font-family: '{}';\n".format(font.name) 
#    svg_head += 10 * " " + "src: url('{}');\n".format(font.fpath) 
#    if (font.tnum): 
#        svg_head += 10 * " " + "font-variant-numeric: tabular_nums;\n" 
#    svg_head += 8 * " " + "}\n\n" 
#    
#    svg_head += 8 * " " + "text {\n" 
#    svg_head += 10 * " " + "font-size: {}pt;\n".format(font.pt_size) 
#    svg_head += 10 * " " + "text-anchor: end;\n" 
#    svg_head += 8 * " " + "}\n" 
#    svg_head += 6 * " " + "]]>\n" 
#    
#    svg_head += 4 * " " + "</style>\n" 
#    svg_head += 2 * " " + "</defs>\n\n" 

    svg_head += 2 * " " + "<style>\n"
    
    svg_head += 4 * " " + "text {\n" + \
                6 * " " + "font-family: '{}';\n".format(font.name) + \
                6 * " " + "src: local('{}');\n".format(font.name) 
    if(font.tnum): 
        svg_head += 6 * " " + "font-variant-numeric: tabular_nums;\n"
    svg_head += 6 * " " + "font-size: {}pt;\n".format(font.pt_size) 
    svg_head += 6 * " " + "text-anchor: end;\n" 
    svg_head += 6 * " " + "fill: #FFFFFF;\n"
    svg_head += 4 * " " + "}\n"     
    svg_head += 2 * " " + "</style>\n" 
    
    return svg_head 
    
############################################################################
# 
# Helper function to place each digit in timer display 
# 
# @param x Position on x-axis 
# @param y Position on y-axis 
# @param digit Digit to write 
# @return String with SVG code to place digit 
# 
############################################################################
def svg_digit(x, y, digit): 
    digit_str = "    <text x=\"{}pt\" y=\"{}pt\">{}".format(x, y, digit) + \
                "</text>\n"
    return digit_str 

############################################################################  
# 
# Helper function to generate SVG code for timer display. 
# 
# @param font TimerFont object 
# @param hhmmss Time to display, as string HH:MM:SS 
# @return String displaying time
# 
############################################################################
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
 
############################################################################
# 
# Helper function to generate SVG code for time display.
# 
# Yeah, there's a lot of unnecessary decomposition, but I might change my 
# mind later and I want to minimize my refactoring.
# 
# @param font TimerFont object 
# @param hhmmss Time to display, as string HH:MM:SS 
# @return SVG code, as string
# 
############################################################################
def build_svg(font, hhmmss): 
    height = font.ascent - font.descent + 2 * font.lineGap 
    width = (2 * font.adv_col) + (6 * font.adv_dig)
    svg = svg_header(font, width, height) 
    svg += svg_digit_display(font, hhmmss) 
    svg += "</svg>" 
    return svg 

############################################################################
# 
# Helper function to generate SVG file for time display. 
# 
# @param font TimerFont object
# @param hhmmss Time to display, as string HH:MM:SS 
# @param filename Filename to write to, minus extension, as string
# 
############################################################################    
def make_svg_file(font, hhmmss, filename): 
    svg_text = build_svg(font, hhmmss) 
    svgfile = open(filename + ".svg", "w") 
    svgfile.write(svg_text) 
    svgfile.close() 
    return     

############################################################################
# 
# Helper function to generate PNG file from SVG file.  Uses Inkscape.   
# 
# @param filename Filename string, minus extension, for SVG and PNG files.
# 
############################################################################ 
def svg_to_png(filename): 
    #print("Making shell call!")
    shell_call_args = ["inkscape", \
                        filename + ".svg", \
                        "-b", "#000000", \
                        "-e", filename + ".png"] 
    shell_call = subprocess.run(shell_call_args, \
                    timeout = 10, \
                    shell = False) 
    #print(shell_call.stdout) 
#    print("Made shell call!") 
#    print()
    return 

###########################################################################
# 
# Make the image file for current time to display.  Uses all of the above 
# redundant functions.
# 
# @param font TimerFont object 
# @param hhmmss Time to display, as string HH:MM:SS 
# @param filename Filename to write to, as string, without extension
# 
###########################################################################   
def make_img_file(font, hhmmss, filename): 
    #print("Making SVG") 
    make_svg_file(font, hhmmss, filename) 
    #print("Making PNG") 
    svg_to_png(filename) 
    return 