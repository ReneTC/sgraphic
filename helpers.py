from PIL import ImageColor # convert hex to rgb
from .main import *

def get_rgb(hex):
    '''
    Get rgb values from HEX string.
    '''
    return ImageColor.getcolor(hex, "RGB")
