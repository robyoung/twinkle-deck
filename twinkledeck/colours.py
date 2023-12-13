RED = (99, 0, 0)
GREEN = (0, 99, 0)
BLUE = (0, 0, 99)
ORANGE = (99, 33, 0)
PURPLE = (99, 0, 99)
YELLOW = (99, 66, 0)
LIME = (99, 120, 0)
CYAN = (0, 99, 66)
WHITE = (99, 99, 99)


def rgb_to_hsv(red, green, blue):
    """Convert RGB to HSV (hue, saturation, value/brightness)"""
    # Based on https://www.rapidtables.com/convert/color/
    # rgb-to-hsv.html
    red = red / 255
    green = green / 255
    blue = blue / 255
    c_max = max(red, green, blue)
    c_min = min(red, green, blue)
    delta = c_max - c_min
    hue = 0
    saturation = 0
    value = c_max
    if delta != 0:
        if c_max == red:
            hue = 60 * (((green - blue) / delta) % 6)
        elif c_max == green:
            hue = 60 * (((blue - red) / delta) + 2)
        elif c_max == blue:
            hue = 60 * (((red - green) / delta) + 4)

    if c_max != 0:
        saturation = delta / c_max

    return hue / 360.0, saturation, value
