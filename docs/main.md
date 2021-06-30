Module main
===========

Functions
---------

    
`animate(frames)`
:   

    
`get_paint_path(color, linewidth)`
:   Returns skia.paint object for paths (lines etc)

    
`get_paint_polygon(color)`
:   Returns a skia.paint object for polygons (cube, text etc)

    
`get_rgb(hex)`
:   Get rgb values from HEX string.

    
`save(path)`
:   Saves the current scene as image.

    
`show(inline=False)`
:   Shows the scene with all elements drawn.

Classes
-------

`circle(x, y, radius, **kwargs)`
:   

    ### Ancestors (in MRO)

    * main.polygon

    ### Methods

    `draw(self)`
    :

`cube(x, y, width, height, **kwargs)`
:   

    ### Ancestors (in MRO)

    * main.polygon

    ### Methods

    `draw(self)`
    :

`line(x, y, x2, y2, **kwargs)`
:   

    ### Ancestors (in MRO)

    * main.path

    ### Methods

    `draw(self)`
    :

`path(x, y, **kwargs)`
:   

    ### Descendants

    * main.line

    ### Methods

    `show(self)`
    :

`polygon(x, y, **kwargs)`
:   

    ### Descendants

    * main.circle
    * main.cube
    * main.text

    ### Methods

    `show(self)`
    :

`scene(width, height, **kwargs)`
:   A class to represent the scene.

    ### Methods

    `draw_objects(self, element)`
    :

    `reset(self)`
    :   Resets all elements to initial scene.

`text(x, y, message, **kwargs)`
:   

    ### Ancestors (in MRO)

    * main.polygon

    ### Methods

    `draw(self)`
    :