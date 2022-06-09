import skia
import contextlib
from IPython.display import display
from PIL import Image # show image in terminal
import os

from .helpers import *


class make_scene:
    '''
    A class to represent the scene.
    '''
    def __init__(self,width,height,**kwargs):
        self.width = width
        self.height = height
        self.color = kwargs.get('color', '#ffffff')
        self.frames = kwargs.get('frames', 1)
        self.alpha = kwargs.get('alpha', 255)
        self.frame = 0
        self.rgb = get_rgb(self.color)
        self.draw_elements = []
        self.alpha = 0

        self.reset()

    def reset(self):
        '''
        Resets all elements to initial scene.
        '''
        self.code ='''
width, height = '''+str(self.width)+''',  '''+str(self.height)+'''
surface = skia.Surface(width, height)
with surface as canvas:
    canvas.translate('''+str(self.width/2)+''', '''+str(self.height/2)+''')
    canvas.clear(skia.ColorSetARGB('''+str(self.alpha)+''','''+str(self.rgb[0])+''','''+str(self.rgb[1])+''', '''+str(self.rgb[2])+'''))'''
        exec(self.code, globals())

    def draw_objects(self, element):
        self.draw_elements.append(element)

frames = 10

def scene(width,height,frames=1,alpha=255):
    '''
    updates scene without makeing new class instance
    '''
    # put global var the_scene here maybe?
    the_scene.width = width
    the_scene.height = height
    the_scene.frames = frames
    the_scene.alpha = alpha
    the_scene.draw_elements = []
    the_scene.reset()

# make the one scene a global variable
the_scene = make_scene(500,250)
class translate:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        the_scene.draw_objects(self)

    def draw(self):
        canvas.translate(self.x,- self.y)

class rotate:
    def __init__(self,angle):
        self.angle = angle
        the_scene.draw_objects(self)

    def draw(self):
        canvas.rotate(self.angle)

class scale:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        the_scene.draw_objects(self)

    def draw(self):
        canvas.scale(self.x,self.y)

class push:
    def __init__(self):
        the_scene.draw_objects(self)

    def draw(self):
        canvas.save()

class pop:
    def __init__(self):
        the_scene.draw_objects(self)

    def draw(self):
        canvas.restore()

def take_screenshot():
    '''
    renders all elements to scene
    '''
    with surface as canvas:
        for draw_objects in the_scene.draw_elements:
            draw_objects.draw()
    screenshot = surface.makeImageSnapshot()
    the_scene.reset()
    return screenshot

def show(inline=False):
    '''
    Shows the scene with all elements drawn.
    '''
    screenshot = take_screenshot()
    if inline == False:
        img = Image.fromarray(screenshot)
        img.show()
    else:
        display(screenshot)

def save(path):
    '''
    Saves the current scene as image.
    '''
    screenshot = take_screenshot()
    screenshot.save(path, skia.kPNG)

def saver(frame,filename=None):
    '''
    saves all frames. in same directory as callign file. filename/filename0001.png
    '''
    import pathlib
    from sys import argv
    import os
    if filename == None:
        filename = os.path.basename(os.path.splitext(argv[0])[0])
    path = pathlib.Path().absolute()
    isfile = os.path.join(path,filename)

    if not os.path.exists(isfile):
        os.makedirs(isfile)

    save(os.path.join(path,filename,str(filename) + str(frame).zfill(3) + ".png"))


class image:
    def __init__(self,x,y,path,**kwargs):
        self.x = x
        self.y = y
        self.image = skia.Image.open(path)
        self.alpha = kwargs.get('alpha', 1.0)
        self.width = kwargs.get('width', self.image.width())
        self.height = kwargs.get('height', self.image.height())
        the_scene.draw_objects(self)
        self.rect = skia.Rect(0, 0,0,0).MakeXYWH(self.x,-self.y,self.width,self.height)
        self.paint = skia.Paint(
                AntiAlias=True,
                Alphaf=self.alpha
        )

    def draw(self):
        canvas.drawImageRect(self.image, self.rect, self.paint)

# load graphic elements
exec(open(os.path.join(os.path.dirname(__file__), 'polygon.py')).read())
exec(open(os.path.join(os.path.dirname(__file__), 'path.py')).read())
