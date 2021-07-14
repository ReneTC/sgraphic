import skia
import contextlib
from IPython.display import display
from PIL import Image # show image in terminal

from .helpers import *

#pdoc -o ./docs ./main.py --force

class scene:
    '''
    A class to represent the scene.
    '''

    def __init__(self,width,height,**kwargs):
        self.width = width
        self.height = height
        self.color = kwargs.get('color', '#ffffff')
        self.rgb = get_rgb(self.color)
        self.draw_elements = []
        self.code ='''
width, height = '''+str(self.width)+''',  '''+str(self.height)+'''
surface = skia.Surface(width, height)
with surface as canvas:
    canvas.clear(skia.ColorSetRGB('''+str(self.rgb[0])+''','''+str(self.rgb[1])+''', '''+str(self.rgb[2])+'''))'''

        self.reset()
        # global _scene

    def reset(self):
        '''
        Resets all elements to initial scene.
        '''
        exec(self.code, globals())

    def draw_objects(self, element):
        self.draw_elements.append(element)

the_scene = scene (500,250)

def take_screenshot():
    '''
    renders all elements to scene
    '''
    for draw_objects in the_scene.draw_elements:
        draw_objects.show()
    screenshot = surface.makeImageSnapshot()

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


def get_paint_polygon(color):
    '''
    Returns a skia.paint object for polygons (cube, text etc)
    '''
    rgb = get_rgb(color)
    color = Color=skia.ColorSetRGB(rgb[0], rgb[1], rgb[2])
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
        with surface as canvas:
            self.draw()

class cube(polygon):
    def __init__(self, x, y,width, height, **kwargs):
        super().__init__(x, y,**kwargs)
        self.width = width
        self.height = height

    def draw(self):
        canvas.drawRect(skia.Rect.MakeXYWH(self.x, self.y, self.width, self.height), self.paint)

class circle(polygon):
    def __init__(self, x, y, radius, **kwargs):
        super().__init__(x, y, **kwargs)
        self.radius = radius

    def draw(self):
        canvas.drawCircle(self.x,self.y, self.radius, self.paint)

class text(polygon):
    def __init__(self, x, y, message, **kwargs):
        super().__init__(x, y, **kwargs)
        self.message = message
        self.font_size = kwargs.get('font_size', 36)
        self.blob = skia.TextBlob(self.message, skia.Font(None, self.font_size))

    def draw(self):
        canvas.drawTextBlob(self.blob, self.x, self.y, self.paint)



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
        with surface as canvas:
            self.draw()


class line(path):
    def __init__(self, x, y, x2,y2,**kwargs):
        super().__init__(x, y, **kwargs)
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        path = skia.Path()
        path.moveTo(self.x, self.y)
        path.lineTo(self.x2, self.y2)
        path.close()
        canvas.drawPath(path, self.paint)

def animate(frames):
    global frame
    frame = 0
    while frame < frames:
        the_scene.reset()
        animation()

        save("test/"+str(frame)+".png")
        frame += 1
