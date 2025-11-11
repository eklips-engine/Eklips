# Import libraries
import pygame, pyglet as pg, json, gc
from classes import ui

# Import inherited
from classes.nodes.gui.canvasitem import *

# Classes
class ColorRect(CanvasItem):
    """
    ## A 2D Sprite.
    
    XXX
    """
    _can_check_layer = True
    base_properties  = {
        "name":      "ColorRect",
        "transform": base_transform,
        "color":     [0,0,0],
        "script":    None
    }

    def __init__(self, properties=base_properties, parent=None):
        super().__init__(properties, parent)
        self.set_color(*self.get("color", [0,0,0]))
        self._make_new_sprite()
    
    def set_color(self, rgb):
        self.image = pg.image.ImageData(1,1,'RGB',bytes(rgb))
    
    def update(self):
        super().update()
        self.draw(self.image)