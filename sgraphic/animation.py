from easing_functions import *
import numpy as np
from .main import the_scene
from .helpers import *
def interpolate(start_val,end_val,when_frame,duration = 20):
    '''
    returns only 1 value at a time
    '''
    frame = the_scene.frame
    if frame < when_frame:
        return start_val

    elif frame < when_frame + duration:
        a = ExponentialEaseInOut(start=start_val, end=end_val, duration=duration)
        return a.ease(frame-when_frame)

    else:
        return end_val

def interpolate_color(start_val,end_val,when_frame,duration = 20):
    '''
    returns only 1 value at a time
    '''
    frame = the_scene.frame

    r1, g1, b1 = get_rgb(start_val)
    r2, g2, b2 = get_rgb(end_val)

    if frame < when_frame:
        return start_val

    elif frame < when_frame + duration:
        r = ExponentialEaseInOut(start=r1, end=r2, duration=duration)
        g = ExponentialEaseInOut(start=g1, end=g2, duration=duration)
        b = ExponentialEaseInOut(start=b1, end=b2, duration=duration)
        r_f = int(r.ease(frame-when_frame))
        r_g = int(g.ease(frame-when_frame))
        r_b = int(b.ease(frame-when_frame))

        return get_hex((r_f,r_g,r_b))

    else:
        return end_val


def interpolate_array(start_val,end_val,when_frame, duration = 20):
    '''
    returns array of data
    '''
    frames = the_scene.frames
    start_values = np.ones(when_frame)*start_val
    end_values = np.ones(frames-duration)*end_val
    transition_values = np.ones(duration)

    a = ExponentialEaseInOut(start=0, end=1, duration=duration)

    for i in range(0,duration):
        transition_values[i] = a.ease(i)*end_val
    return np.concatenate((start_values,transition_values,end_values))

def switch(start_val,end_val,when_frame,frame):
    return interpolate(start_val,end_val,when_frame,frame,duration = 0)

def hold_switch(start_val,end_val,when_frame,frame, hold = 20):
    if frame < when_frame:
        return start_val

    elif frame < when_frame + hold:
        return end_val

    else:
        return start_val

def boolean_pulse(period,frame,offset=0,on_val = 1, off_val = 0):
    if (frame/(period+offset)).is_integer() == 1:
        return on_val
    else:
        return off_val


animation_code = '''
def show_animation(inline=False,frame = 0):
    animation()
    the_scene.frame = frame
    show(inline)

def animate(filename=None):
    while the_scene.frame < the_scene.frames:
        global frame
        frame = the_scene.frame
        the_scene.reset()
        animation()
        saver(the_scene.frame,filename)
        the_scene.frame += 1
        print(the_scene.frame)
'''
