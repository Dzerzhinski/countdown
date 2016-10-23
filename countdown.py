from moviepy.editor import *
from numpy import *

import subprocess 

SCREENSIZE = (1280, 720)
HOURS = 1
MIN_PER_HOUR = 60
SEC_PER_MIN = 60
TIME_FMT = '{:02d}:{:02d}:{:02d}' 

FONTSIZE = 200

font_name = "monofur"

hour = 1
minute = 0
second = 0

#clip_queue = []


def find_font_file(font_name): 
    shell_call_args = ["convert", "-list", "font"] 
    shell_call = subprocess.Popen(shell_call_args, stdout = subprocess.PIPE) 
    font_list, shell_err = shell_call.communicate() 
    
    fname_exp = r"^Font: " + font_name + r"$" 
    fpath_exp = r"\bglyphs: (.*)$" 
    
    fname_match = re.search(fname_exp) 
    fpath_match = re.search(fpath_exp, fname_match.start) 
    
    return fpath_match.group(1) 

ttl_time = ((hour * 60) + minute) * 60 + second

#clip_15m = VideoFileClip("clips/Scene2.mov").set_start((10, 0))
#clip_30m = VideoFileClip("clips/Scene3.mov").set_start((20, 0))
#clip_45m = VideoFileClip("clips/Scene4.mov").set_start((30, 0))



# def calc_start(h, m, s):
#     minutes = (MINUTES - 1) - m
#     seconds = 59 - s
#     return (h, minutes, seconds)
# 
# def calc_end(h, m, s):
#     seconds = 60 - s
#     minutes = (MINUTES - 1) - m + (seconds // 60)
#     seconds = seconds % 60
#     return (h, minutes, seconds)

def prnt_time_left(current_time):
    time = ttl_time - current_time
    s = time % 60
    time = time // 60
    m = time % 60
    time = time // 60
    h = time
    return TIME_FMT.format(h, m, s)

file_queue = []
n = 0
flag = False
while (not flag):
    clip_queue = []
    for i in range(60):
        if(((n * 60) + i) > ttl_time): 
            break
        time = prnt_time_left((60 * n) + i)
        clip = TextClip(time, font = font_name, color = 'white', \
                fontsize = FONTSIZE).set_pos('center')
        clip = clip.set_start(i)
        clip = clip.set_end(i + 1)
        clip_queue.append(clip)
    subfile = CompositeVideoClip(clip_queue, size = SCREENSIZE, bg_color = (0, 0, 0))
    subfile.write_videofile("countdown_subfile{number}.mp4".format(number = n), fps = 24, threads = 1)
    file_queue.append(VideoFileClip("countdown_subfile{number}.mp4".format(number = n)).set_start((n, 0)))
    clip_queue = []
    subfile = None
    n += 1
    if(n * 60 > ttl_time):
        flag = True

end_clip = TextClip("00:00:00", \
        font = font_name, color = 'white', \
        fontsize = FONTSIZE).set_pos('center')
end_clip = end_clip.set_start(ttl_time)
end_clip = end_clip.set_duration(60)
file_queue.append(end_clip)

# for i in reversed(range(0, hour)):
#     for j in reversed(range(MINUTES)):
#         for k in reversed(range(SECONDS)):
#             time = TIME_FMT.format(i, j, k)
#             clip = TextClip(time, font = 'Eraser', color = 'white', \
#                     fontsize = 100).set_pos('center')
#             clip = clip.set_start(calc_start(i, j, k))
#             clip = clip.set_end(calc_end(i, j, k))
#             clip_queue.append(clip)

#bg = ColorClip(SCREENSIZE).set_duration(ttl_time + 60)
#file_queue.insert(0, bg)
# countdown = concatenate_videoclips(clip_queue).set_pos('center')

#clip_queue.append(clip_15m)
#clip_queue.append(clip_30m)
#clip_queue.append(clip_45m)

countdown_final = CompositeVideoClip(file_queue, size = SCREENSIZE, bg_color = (0, 0, 0))
countdown_final.write_videofile('countdown.seance.mono.mp4', fps = 24, threads = 4)



