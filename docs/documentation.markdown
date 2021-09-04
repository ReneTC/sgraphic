---
layout: page
title: Documentation
permalink: /documentation/
---
# Example
<p align="center"><img src="img/example.png"></p>
# General
### Scene
A scene must be created to draw elements to.
```
scene(x,y)
Parameters
----------
x : int
    Width of image
y : int
    Height of image
```
```
from sgraphic import *
scene(500,300)
```
### Show
display what is drawn on the scene
```
show()
Parameters
----------
inline(optinal) : Bool
If true, displays image inline
```
```
from sgraphic import *
scene(500,300)
cube(0,100,200,15)
show()
```


# Objects to draw
### circle

```
circle(x,y,radius)
Parameters
----------
x : float
y : float
radius : float

color(optional) : str HEX
```
```
from sgraphic import *
scene(500,300)
circle(0,0,50, color='#dadada')
show()

```

### cube

```
cube(x,y,w,h)
Parameters
----------
x : float
y : float
w : float
h : float

color(optional) : str HEX
```
```
from sgraphic import *
scene(500,300)
cube(0,0,100,100, color='#dadada')
show()


```
### text
```
text(x,y,text)
Parameters
----------
x : float
y : float
text : str

color(optional) : str HEX
font(optional) : str PATH TO
size(optional) : int
```
```
from sgraphic import *
scene(500,300)
text(0,0,"ZAP")
show()
```

### image
```
image(x,y,path)
Parameters
----------
x : float
y : float
path : float
```
```
from sgraphic import *
scene(500,300)
image(0,0,path/to/image.png)
show()
```

### line
```
line(x1,y1,x2,y2)
Parameters
----------
x1 : float
y1 : float
x2 : float
y2 : float

linewidth(optional) : int
color(optional) : str HEX
```
```
from sgraphic import *
scene(500,300)
line(0,0,100,100)
show(inline=True)
```
# More

### save
```
save(path/to/output.png)
```
### translate
```
translate(x,y)
```
### rotate
```
rotate(deg)
```
### scale
```
scale(x,y)
```
### push
```
push()
```
### pop
```
pop()
```

# Animation
Works and documentation is on the way.. but currently it is a little messy.
