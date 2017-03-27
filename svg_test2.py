# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 00:22:48 2017

@author: johns
"""

import timerDisplay as td  
import timerFont as tf


FONT = "Times New Roman" 
POINTSIZE = 100 

font = tf.TimerFont(FONT, POINTSIZE) 

svg_text = td.build_svg(font, td.time_to_str(200))

f = open("bar2.svg", "w") 
f.write(svg_text) 
f.close()