## Import singleton
import pyglet as pg
from classes.resources.resource import *
from classes.types              import *

## Classes
class Tileset(Resource):
    """
    An image with a set of Tiles used to make a Tilemap.
    """

    ## Exported properties
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, img : pg.image.ImageData):
        self._image   = img
        self._texture = img.get_texture()
    
    @export(None,"str","file_path/img")
    def image_path(self):
        return self._imagepath
    @image_path.setter
    def image_path(self, value):
        if not value: return
        self._imagepath = value
        self.image      = engine.loader.load(value)
    
    @export([16,16], "list", "vector2/wh")
    def grid_size(self):
        return self._gridsize
    @grid_size.setter
    def grid_size(self, value):
        self._gridsize = value
    
    @export({},"dict","tiles")
    def tiles(self) -> dict:
        return self._tiles
    @tiles.setter
    def tiles(self, value : dict):
        # {Tile: [x, y]}
        self._tiles = value
    
    ## UV
    def get_uv(self, tid):
        tx, ty = self._tiles[tid]

        tw, th = self._gridsize
        iw, ih = self._image.width, self._image.height

        u0 = (tx * tw)     / iw
        v0 = (ty * th)     / ih
        u1 = ((tx+1) * tw) / iw
        v1 = ((ty+1) * th) / ih

        return [
            u0, v0, 0,
            u1, v0, 0,
            u1, v1, 0,
            u0, v1, 0
        ]
    
    ## Texture
    @property
    def texture(self):
        return self._texture
    
    ## Init
    def __init__(self, properties={}):
        self._image     = None
        self._texture   = None
        self._gridsize  = [16,16]
        self._imagepath = None
        self._tiles     = {}

        super().__init__(properties)