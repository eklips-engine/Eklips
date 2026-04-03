## Functions
def rgbtohex(rgb: list) -> str:
    """Turn a hex color into an RGB color."""
    r,g,b = rgb
    return "#{:02x}{:02x}{:02x}".format(round(r),round(g),round(b))
def invertrgb(rgb: list) -> list:
    """Invert an RGB color."""
    r,g,b = rgb
    return [255-r,255-g,255-b]

## Classes
class Color:
    """A color container."""
    def __init__(self, r=0,g=0,b=0,a=255):
        self._r = r
        self._g = g
        self._b = b
        self._a = a
    def color_as_tuple(self):
        """Return the color as a tuple."""
        return (self.r, self.g, self.b, self.a)
    def color_as_list(self):
        """Return the color as a list."""
        return [self.r, self.g, self.b, self.a]

    @property
    def r(self):
        """Red."""
        return self._r
    @property
    def g(self):
        """Green."""
        return self._g
    @property
    def b(self):
        """Blue."""
        return self._b
    @property
    def a(self):
        """Alpha."""
        return self._a

    @r.setter
    def r(self, value):
        self._r = int(value)
        self._update_color(*self.color_as_list())
    @g.setter
    def g(self, value):
        self._g = int(value)
        self._update_color(*self.color_as_list())
    @b.setter
    def b(self, value):
        self._b = int(value)
        self._update_color(*self.color_as_list())
    @a.setter
    def a(self, value):
        self._a = int(value)
        self._update_color(*self.color_as_list())
    
    def _update_color(self, r,g,b,a):
        return

    ## Exports
    @property
    def rgb(self):
        """RGBA color value as a list. Read-write.
        
        Due to Python limitations, this can only be modified by doing `self.rgb = ...` and not `self.rgb[X] = ...`."""
        return self.color_as_list()
    @rgb.setter
    def rgb(self, rgbv):
        self._r, self._g, self._b = rgbv[:3]
        if len(rgbv) > 3:
            self._a = rgbv[3]
        self._update_color(*self.color_as_list())