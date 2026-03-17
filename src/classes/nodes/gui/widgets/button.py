# Import libraries
from classes.nodes.gui.ninepatchrect import *

# Classes
class Button(BaseNinePatchRect, Color):
    """
    A themed Button.
    """
    _isblittable = True

    ## Exported properties
    @export("Button","str","str")
    def text(self) -> str: return self._text
    @text.setter
    def text(self, value):
        self._text = value
        if self.label:
            self.label.text = value

    @export(DEFAULT_FONT_NAME,"str","font")
    def font(self) -> str: return self._fname
    @font.setter
    def font(self, value):
        self._fname = value
        if self.label:
            self.label.font_name = value

    @export(DEFAULT_FONT_SIZE,"float/int","float/int")
    def font_size(self) -> float | int: return self._fsize
    @font_size.setter
    def font_size(self, value):
        self._fsize = value
        if self.label:
            self.label.font_size = value

    @export(WHITE,"list","color")
    def color(self) -> tuple[int, int, int]:
        """RGBA Color value of the text. Modifying a single item will do nothing."""
        return self.color_as_tuple()
    @color.setter
    def color(self, rgb : tuple[int, int, int] | list[int]):
        self.rgb = rgb
    def _update_color(self, r, g, b, a):
        if self.label:
            self.label.color = (r,g,b,a)
    
    ## CItem Management
    def _remove_item(self):
        if self.citem:
            self.citem.delete()
            self.citem = None
    def _make_new_item(self):
        self.label = pg.text.Label(batch=self.batch)
        
        self.label.color     = self.color
        self.label.text      = self.text
        self.label.font_name = self.font
        self.label.font_size = self.font_size
        super()._make_new_item()
    def _set_alpha(self, deg):
        super()._set_alpha(deg)
        self.label.opacity = deg
    def _set_visible(self, val):
        super()._set_visible(val)
        self.label.visible = val
    
    ## Init
    def draw(self):
        super().draw()
        if self.visible and self.viewport.is_onscreen(self) and self.citem:
            x, y         = self.into_screen_coords()
            self.label.x = x+(self.w/2-self.label.content_width/2)
            self.label.y = y+(self.h/2-self.label.content_height/2)

    def __init__(self, properties={}, parent=None):
        Color.__init__(self, *WHITE)
        self._text  = "Text"
        self._fsize = DEFAULT_FONT_SIZE
        self._fname = DEFAULT_FONT_NAME
        self.label  = None

        super().__init__(properties, parent)

        self._corner_size = engine.theme.get_widget_data("button")["corner_size"]
        self._edge_size   = engine.theme.get_widget_data("button")["side_size"]
        self.image        = engine.theme.get_static_widget("button")