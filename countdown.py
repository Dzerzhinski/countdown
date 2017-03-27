# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 13:25:44 2017

@author: johns
"""

from moviepy.editor import * 
from timerFont import *
import timerDisplay as TD 

SCREENSIZE = (1280, 720)
HOURS = 1
MIN_PER_HOUR = 60
SEC_PER_MIN = 60 

FONTSIZE = 200  

SUBCLIP_INCR = 60

font_name = "Times New Roman"
output_file = "countdown.mp4" 
font_file = "c:\\Windows\\Fonts\\times.ttf" 

hour = 0
minute = 0
second = 10 

def make_subclip(font, ttl_time, i_clip): 
    img_queue = [] 
    for j in range(SUBCLIP_INCR): 
        if(j + (i_clip * SUBCLIP_INCR) > ttl_time): 
            break 
        time = (i_clip * SUBCLIP_INCR) + j 
        time_display_str = TD.time_to_str(TD.get_time_left(ttl_time, time)) 
        img_file_j = "./temp/temp_timer{}".format(j) 
        TD.make_img_file(font, time_display_str, img_file_j)  
        img_clip_j = ImageClip(img_file_j + ".png").set_position("center") 
        img_clip_j = img_clip_j.set_start((j)) 
        img_clip_j = img_clip_j.set_end((j + 1)) 
        img_queue.append(img_clip_j) 
    subclip = CompositeVideoClip(img_queue, bg_color = (0, 0, 0)) 
    subclip_file = "./temp/subclip{}.mp4".format(i_clip) 
    subclip.write_videofile(subclip_file, fps = 24) 
    return subclip_file
    
def make_file(font, ttl_time, outfile): 
    subclip_queue = list() 
    zero_flag = False 
    i_subclip = 0 
    while(not zero_flag): 
        subclip = make_subclip(font, ttl_time, i_subclip) 
        t_subclip = SUBCLIP_INCR * i_subclip
        subclip_queue.append(VideoFileClip(subclip).set_start(t_subclip).set_position("center")) 
        i_subclip += 1 
        zero_flag = (i_subclip * SUBCLIP_INCR > ttl_time) 
    countdown = CompositeVideoClip(subclip_queue, size = SCREENSIZE, \
                    bg_color = (0, 0, 0)) 
    countdown.write_videofile(outfile, fps = 24) 
    

font = TimerFont(font_name, font_file, FONTSIZE) 
countdown_length = (hour * MIN_PER_HOUR) 
countdown_length = SEC_PER_MIN * (minute + countdown_length) 
countdown_length += second 

make_file(font, countdown_length, output_file) 