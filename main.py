import skia
import contextlib
from IPython.display import display
from PIL import Image # show image in terminal
import os

from .helpers import *

#pdoc -o ./docs ./main.py --force

class make_scene:
    '''
    A class to represent the scene.
    '''

    def __init__(self,width,height,**kwargs):
        self.width = width
        self.height = height
        self.color = kwargs.get('color', '#ffffff')
        self.rgb = get_rgb(self.color)
        self.draw_elements = []


        self.reset()
        # global the_scene

    def reset(self):
        '''
        Resets all elements to initial scene.
        '''
        self.code ='''
width, height = '''+str(self.width)+''',  '''+str(self.height)+'''
surface = skia.Surface(width, height)
with surface as canvas:
    canvas.translate('''+str(self.width/2)+''', '''+str(self.height/2)+''')
    canvas.clear(skia.ColorSetRGB('''+str(self.rgb[0])+''','''+str(self.rgb[1])+''', '''+str(self.rgb[2])+'''))'''
        exec(self.code, globals())

    def draw_objects(self, element):
        self.draw_elements.append(element)
frames = 10
def scene(width,height):
    '''
    updates scene without makeing new class instance
    '''
    the_scene.width = width
    the_scene.height = height
    the_scene.draw_elements = []
    the_scene.reset()

# make the one scene a global variable
the_scene = make_scene(500,250)



def scale():
    with surface as canvas:
        canvas.scale(0.25,0.25)

def push():
    with surface as canvas:
        canvas.save()

def pop():
    with surface as canvas:
        canvas.restore()


def take_screenshot():
    '''
    renders all elements to scene
    '''
    with surface as canvas:
        for draw_objects in the_scene.draw_elements:
            draw_objects.show()
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

def get_paint_polygon2(color):
    '''
    Returns a skia.paint object for polygons (cube, text etc)
    '''
    rgb = get_rgb(color)
    color = skia.ColorSetRGB(rgb[0], rgb[1], rgb[2])
    paint = skia.Paint(
    AntiAlias=True,
    Color=color,
    Style=skia.Paint.kFill_Style,
    )
    return paint


class image:
    def __init__(self,x,y,width,height,**kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        the_scene.draw_objects(self)
        self.image = skia.Image.open('/home/renec/Drive/Higgsino/new_project/vid_files/2_mnist/src/images.png')
        self.rect = skia.Rect(self.x, self.y,self.width,self.height)
        self.paint = skia.Paint(
                AntiAlias=True,
        )

    def show(self):
        self.draw()

    def draw(self):
        canvas.drawImageRect(self.image, self.rect, self.paint)

def get_paint_polygon(color):
    '''
    Returns a skia.paint object for polygons (cube, text etc)
    '''
    rgb = get_rgb(color)
    color = skia.ColorSetRGB(rgb[0], rgb[1], rgb[2])
    paint = skia.Paint(
    AntiAlias=True,
    Color=color,
    Style=skia.Paint.kFill_Style,
    )
    return paint


class polygon:
    def __init__(self,x,y,**kwargs):
        self.x = x
        self.y = y
        self.color = kwargs.get('color', '#000000')
        self.paint = get_paint_polygon(self.color)
        the_scene.draw_objects(self)

    def show(self):
        self.draw()

class cube(polygon):
    def __init__(self, x, y,width, height, **kwargs):
        super().__init__(x, y,**kwargs)
        self.width = width
        self.height = height

    def draw(self):
        canvas.drawRect(skia.Rect.MakeXYWH(self.x, -self.y, self.width, -self.height), self.paint)

class circle(polygon):
    def __init__(self, x, y, radius, **kwargs):
        super().__init__(x, y, **kwargs)
        self.radius = radius

    def draw(self):
        canvas.drawCircle(self.x,-self.y, self.radius, self.paint)

class text(polygon):
    def __init__(self, x, y, message, **kwargs):
        super().__init__(x, y, **kwargs)
        self.message = message
        self.size = kwargs.get('size', 36)
        self.font_type = kwargs.get('font', 'Arial')

        # make custom ttf font and skia fonts
        skia_font = None
        if self.font_type.split('.')[-1] == 'ttf':
            skia_font = skia.Typeface.MakeFromFile(self.font_type)
        else:
            print("what")
            skia_font = skia.Typeface(self.font_type)
        font = skia.Font(skia_font, self.size)

        self.blob = skia.TextBlob(self.message, font)

    def draw(self):
        canvas.drawTextBlob(self.blob, self.x, -self.y, self.paint)



def get_paint_path(color,linewidth):
    '''
    Returns skia.paint object for paths (lines etc)
    '''
    rgb = get_rgb(color)
    color = Color=skia.ColorSetRGB(rgb[0], rgb[1], rgb[2])
    paint = skia.Paint(
        AntiAlias=True,
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=linewidth,
        Color=color,
        StrokeCap=skia.Paint.kRound_Cap,
    )
    return paint


class path:
    def __init__(self,x,y,**kwargs):
        self.x = x
        self.y = y
        self.color = kwargs.get('color', '#000000')
        self.linewidth = kwargs.get('linewidth', 4)
        self.paint = get_paint_path(self.color,self.linewidth)
        the_scene.draw_objects(self)

    def show(self):
        self.draw()


class line(path):
    def __init__(self, x, y, x2,y2,**kwargs):
        super().__init__(x, y, **kwargs)
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        path = skia.Path()
        path.moveTo(self.x, -self.y)
        path.lineTo(self.x2,-self.y2)
        path.close()
        canvas.drawPath(path, self.paint)

class circle_path(path):
    def __init__(self, x, y, radius,**kwargs):
        super().__init__(x, y, **kwargs)
        self.radius = radius

    def draw(self):
        path = skia.Path()
        path.addCircle(self.x, self.y, self.radius)
        path.close()
        canvas.drawPath(path, self.paint)

class cube_path(path):
    def __init__(self, x, y, width,height,**kwargs):
        super().__init__(x, y, **kwargs)
        self.width = width
        self.height = height

    def draw(self):
        path = skia.Path()
        path.addRect((self.x, self.y, self.width, self.height))
        path.close()
        canvas.drawPath(path, self.paint)

animation_code = '''
def animate():
    global frame
    frame = 0
    while frame < frames:
        the_scene.reset()
        animation()
        save("animation/"+str(frame)+".png")
        frame += 1
        print(frame)
'''
exec(animation_code)
