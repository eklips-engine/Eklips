# Import libraries
from classes.resources.tileset    import *
from classes.nodes.gui.canvasitem import *

# Classes
class Tilemap(CanvasItem):
    """
    A grid of tiles placed together to make a map.
    """
    _isblittable = True

    @export({}, "dict", "rsc/Tilemap")
    def tileset(self):
        return self._tileset
    @tileset.setter
    def tileset(self, value):
        self._tileset = engine.loader.load(value)
    @export({}, "dict", "tiles")
    def tiles(self):
        return self._tiles
    @tiles.setter
    def tiles(self, value):
        self._tiles = {}
        for i in value: # TileID, GridX, GridY
            self.place_tile(*i)
    
    def __init__(self, properties={}, parent=None):
        self._tiles = {}
        super().__init__(properties, parent)

        self.batch_id : int     = self.viewport.add_batch()
        self.tileset  : Tileset = None
    
    def draw(self):
        ... # draw it
    
    def update(self):
        ... # add collision boxes using engine.scene.CollisionManager