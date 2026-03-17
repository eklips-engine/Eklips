# Import singleton
import pyglet as pg
from classes.resources.resource import *
from classes.customprops        import *

# Classes
class Tileset(Resource):
    """
    An image with a set of Tiles used to make a Tilemap.
    """

    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, img : pg.image.ImageData):
        self._image   = img
        self.refresh_tiles()
    
    @export(None,"str","file_path/img")
    def image_path(self):
        """Filepath of the attached Image. Setting this value loads and sets the imagepath as the Tileset's image."""
        return self._imagepath
    @image_path.setter
    def image_path(self, value):
        if not value: return
        self._imagepath = value
        self.image      = engine.loader.load(value)
    
    @export({},"dict","sprites")
    def tiles(self) -> dict:
        return self._sprites
    @tiles.setter
    def tiles(self, value : dict):
        self._sprites = {}
        for i in value:
            self._init_tile(self.add_tile(value[i]))
    def add_tile(self, data):
        sid                = len(self._sprites)
        self._sprites[sid] = data
        self._init_tile(sid)

        return sid
    def get_tile_image(self, sid):
        return self._sprites[sid]["image"]
    def _init_tile(self, sid):
        return
    def refresh_tiles(self):
        for i in self._sprites:
            self._init_tile(i)

    def __init__(self, properties={}):
        self._image     = None
        self._imagepath = None
        self._sprites   = {}
        super().__init__(properties)