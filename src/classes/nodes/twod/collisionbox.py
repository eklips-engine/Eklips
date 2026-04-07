## Import libraries
from classes.nodes.gui.colorrect import *

## Classes XXX implement the World
class CollisionBox(CanvasItem):
    """
    A rectangle with Collision abilities.

    This Node uses the `CollisionManager` class, and
    as soon as it is initialized, it adds itself to the
    list.

    This Node uses basic AABB collision cause i'm too
    bad at programming to even bother making collision
    for any other shape than 0deg rectangles
    """

    def __init__(self, properties={}, parent=None):
        super().__init__(properties, parent)
    
    def colliderect(self, shape : Self):
        """Check if two CollisionBoxes are colliding."""
        return self.collides_ui_aabb(shape,
            [self.viewport, None, 1],
            [self.shape.viewport, None, 1])