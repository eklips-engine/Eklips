# Import libraries
import pyglet as pg
from classes.nodes.gui.canvasitem import *

# Classes
class ColorRect(CanvasItem, Color):
    """
    A single-color rectangle on the screen.
    
    XXX
    """
    _isblittable                = True
    citem : pg.shapes.Rectangle = None

    def __init__(self, properties={}, parent=None):
        Color.__init__(self, *WHITE)
        super().__init__(properties, parent)
    
    @export(WHITE,"list","color")
    def color(self) -> tuple[int, int, int]:
        """RGBA Color value of the ColorRect. Modifying a single item will do nothing."""
        return self.color_as_tuple()
    @color.setter
    def color(self, rgb : list[int]):
        if rgb == self.rgb:
            return
        self.rgb = rgb
    
    ## Drawing related
    def update(self):
        super().update()
        self.draw()
    
    ## Transform related
    def _update_color(self, r, g, b, a):
        if self.citem:
            self.citem.color = [r, g, b, a]
    def _set_size(self, w, h):
        if self.citem:
            self.citem.width  = self._w
            self.citem.height = self._h
            self._set_anchors()
    def _set_flip(self, w, h):
        if self.citem:
            self.citem.scale_x = self.scale_x
            self.citem.scale_y = self.scale_y
    def _set_anchors(self):
        self.citem.anchor_x = self.citem.width  // 2
        self.citem.anchor_y = self.citem.height // 2
        self.citem._update_translation()
    
    def _make_new_item(self):
        if self.citem:
            self._remove_item()
        if not self.image:
            self._image = engine.loader.load("root://_assets/error.png")
        self.citem      = pg.shapes.Rectangle(0,0,self._w,self._h, color=self.color, batch=self.batch)
        self._set_anchors()
        self.citem.visible = False