from PIL import ImageColor # convert hex to rgb

def get_rgb(hex):
    '''
    Get rgb values from HEX string.
    '''
    return ImageColor.getcolor(hex, "RGB")
