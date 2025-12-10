# Import libraries
import pygame, pyglet as pg, json, gc
from classes import ui

# Import inherited
from classes.nodes.gui.colorrect import *

# Classes
class CollisionBox(ColorRect):
    """
    ## A rectangle with Collision abilities.
    
    The sole reason 
    """

    def __init__(self, properties={}, parent=None, children=None):
        super().__init__(properties, parent, children)
        self.world = engine.scene._collisionman
        self.rid   = self.world.add(self)
    
    def draw(self, image):
        if engine.debug.shapes_visible and engine.debug.enabled:
            super().draw(image)
    
    def aabb(self):
        return (self.x, self.y, self.x + self.w, self.y + self.h)
    
    def _set_pos(self):
        return
    