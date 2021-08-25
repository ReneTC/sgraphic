from PIL import ImageColor # convert hex to rgb


def get_rgb(hex):
    '''
    Get rgb values from HEX string.
    '''
    return ImageColor.getcolor(hex, "RGB")

def get_hex(rgb):
    '''
    Get rgb values from HEX string.
    '''
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    return "#{:02x}{:02x}{:02x}".format(r,g,b)
