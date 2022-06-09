def get_paint_path(color,linewidth):
    '''
    Returns skia.paint object for paths
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
        path.addCircle(self.x, - self.y, self.radius)
        path.close()
        canvas.drawPath(path, self.paint)

class cube_path(path):
    def __init__(self, x, y, width,height,**kwargs):
        super().__init__(x, y, **kwargs)
        self.width = width
        self.height = height

    def draw(self):
        path = skia.Path()
        path.addRect((self.x-self.width, -self.y+self.height, self.width*2, -self.height*2))
        #below is xywh aligment
        #path.addRect((self.x, -self.y, self.width, -self.height))
        path.close()
        canvas.drawPath(path, self.paint)
