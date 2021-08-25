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
        self.frames = kwargs.get('frames', 1)
        self.alpha = kwargs.get('alpha', 255)
        self.frame = 0
        self.rgb = get_rgb(self.color)
        self.draw_elements = []
        self.alpha = 0

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
    canvas.clear(skia.ColorSetARGB('''+str(self.alpha)+''','''+str(self.rgb[0])+''','''+str(self.rgb[1])+''', '''+str(self.rgb[2])+'''))'''
        exec(self.code, globals())

    def draw_objects(self, element):
        self.draw_elements.append(element)

frames = 10

def scene(width,height,frames=1,alpha=255):
    '''
    updates scene without makeing new class instance
    '''
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
        canvas.translate(self.x,self.y)

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

class vertices:
    def __init__(self,points,**kwargs):
        self.points = points

        self.color = kwargs.get('color', '#000000')
        self.alpha = kwargs.get('alpha', 1.0)

        self.paint = get_paint_polygon(self.color,self.alpha)
        the_scene.draw_objects(self)

        self.skia_points = []
        for p in self.points:
            self.skia_points.append(skia.Point(p[0], - p[1]))

    def draw(self):
        canvas.drawVertices(skia.Vertices(skia.Vertices.kTriangles_VertexMode,self.skia_points),self.paint)


def get_paint_polygon(color,alpha):
    '''
    Returns a skia.paint object for polygons (cube, text etc)
    '''
    rgb = get_rgb(color)
    color = skia.ColorSetRGB(rgb[0], rgb[1], rgb[2])
    paint = skia.Paint(
    AntiAlias=True,
    Color=color,
    Style=skia.Paint.kFill_Style,
    Alphaf=alpha
    )
    return paint


class polygon:
    def __init__(self,x,y,**kwargs):
        self.x = x
        self.y = y
        self.color = kwargs.get('color', '#000000')
        self.alpha = kwargs.get('alpha', 1.0)
        self.paint = get_paint_polygon(self.color,self.alpha)
        the_scene.draw_objects(self)


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
        path.addRect((self.x, -self.y, self.width, -self.height))
        path.close()
        canvas.drawPath(path, self.paint)


def grid():
    line(0,the_scene.height,0,-the_scene.height)
    line(-the_scene.width,0,the_scene.height,0)
