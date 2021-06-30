import skia
import contextlib
from IPython.display import display
from PIL import ImageColor # convert hex to rgb
from PIL import Image # show image in terminal

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
        global scene
        scene = self

    def reset(self):
        '''
        Resets all elements to initial scene.
        '''
        exec(self.code, globals())

    def draw_objects(self, element):
        self.draw_elements.append(element)
        pass

def show(inline=False):
    '''
    Shows the scene with all elements drawn.
    '''
    for draw_objects in scene.draw_elements:
        draw_objects.show()
    snapshot = surface.makeImageSnapshot()

    if inline == False:
        img = Image.fromarray(snapshot)
        img.show()
    else:
        display(snapshot)

def save(path):
    '''
    Saves the current scene as image.
    '''
    for draw_objects in scene.draw_elements:
        draw_objects.show()

    snapshot = surface.makeImageSnapshot()
    snapshot.save(path, skia.kPNG)

def get_rgb(hex):
    '''
    Get rgb values from HEX string.
    '''
    return ImageColor.getcolor(hex, "RGB")

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


class polygon:
    def __init__(self,x,y,**kwargs):
        self.x = x
        self.y = y
        self.color = kwargs.get('color', '#000000')
        self.paint = get_paint_polygon(self.color)
        scene.draw_objects(self)

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

class path:
    def __init__(self,x,y,**kwargs):
        self.x = x
        self.y = y
        self.color = kwargs.get('color', '#000000')
        self.linewidth = kwargs.get('linewidth', 4)
        self.paint = get_paint_path(self.color,self.linewidth)
        scene.draw_objects(self)

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
        scene.reset()
        animation()

        save("test/"+str(frame)+".png")
        frame += 1
