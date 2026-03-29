## Import libraries
from classes.resources.image  import *
from classes.nodes.gui.sprite import *

## Classes
class AnimatedSprite(Animation, CanvasItem):
    """
    A 2D Animated Sprite using the Animation resource.
    """
    _isblittable     = True

    ## Init
    def __init__(self, properties={}, parent=None):
        super().__init__(properties)
        CanvasItem.__init__(self, properties, parent)
    
    def _set_animation_as_image(self):
        self.image = self.get_animation_image(self.animation)
    
    def update(self):
        super().update()
        self.draw()