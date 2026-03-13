## XXX
# Import libraries
from classes.nodes.gui.canvasitem import *

# Classes
class Button(CanvasItem):
    """
    A Button.
    
    XXX
    """
    
    def __init__(self, properties={}, parent=None):
        self._tiles = {}
        super().__init__(properties, parent)

        self.batch_id = self.viewport.add_batch()