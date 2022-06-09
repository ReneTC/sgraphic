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
        canvas.drawRect(skia.Rect.MakeXYWH(self.x-self.width, -self.y+self.height, self.width*2, -self.height*2), self.paint)
        #below is xywh aligment
        #canvas.drawRect(skia.Rect.MakeXYWH(self.x, -self.y, self.width, -self.height), self.paint)

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
