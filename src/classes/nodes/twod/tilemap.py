## Import libraries
import pyglet                     as pg
from classes.resources.tileset    import *
from classes.nodes.gui.canvasitem import *

## XXX implement rendering and collision logic
class Tilemap(CanvasItem):
    _isblittable                                = True
    citem : pg.graphics.vertexdomain.VertexList = None

    ## Exported
    @export({}, "dict", "rsc/Tileset")
    def tileset(self) -> Tileset:
        return self._tileset

    @tileset.setter
    def tileset(self, value):
        self._tileset = engine.loader.load(value)
        self._rebuild()

    @export({}, "dict", "tiles")
    def tiles(self):
        return self._tiles

    @tiles.setter
    def tiles(self, value: dict):
        self._tiles = value
        self._rebuild()

    ## Init
    def __init__(self, properties={}, parent=None):
        self._tiles             = {}
        self._tileset : Tileset = None
        self._latestid          = 0

        self._vertices = []
        self._count    = 0

        super().__init__(properties, parent)
        self._make_new_item()
    
    ## VertexList Management
    def _make_new_item(self):
        if self.citem:
            self.citem.delete()
        if not self.tileset or not self.tiles:
            self.citem = None
            return

        self._drawing_bid  = self.viewport.add_batch()
        self._cached_batch = self.viewport.batches[self.batch_id]
    
    def _rebuild(self):
        if self._tileset == None or not self._tiles:
            self._count = 0
            if self.citem:
                self.citem.resize(0)
            return
        
        gw, gh = self._tileset.grid_size
        
        vertices = []
        texcoords = []
        return

        for (gx, gy), tile_id in self._tiles.items():
            if tile_id == None:
                continue
            if not tile_id in self._tileset.tiles:
                continue
            
            px = gx * gw
            py = gy * gh
            
            quad_verts = [
                px,      py + gh,  # top-left
                px + gw, py + gh,  # top-right
                px + gw, py,      # bottom-right
                px,      py       # bottom-left
            ]
            vertices.extend(quad_verts)
            
            uvs = self._tileset.get_uv(tile_id)
            for i in range(4):
                texcoords.extend([uvs[i*3], uvs[i*3 + 1], uvs[i*3 + 2]])
            
            
            if tile_id < 0:
                self._solid_tiles.add((gx, gy))
        
        # Update vertex list
        quad_count  = len(vertices) // 8
        self._count = len(vertices) // 2
        
        if self.citem:
            self.citem.resize(self._count)
            if vertices:
                self.citem.vertices = vertices
                self.citem.tex_coords = texcoords
        
        self._vertices = vertices

    def _handle_collisions(self):
        return
    def draw(self):
        return

    def update(self):
        super().update()
        self._handle_collisions()
        self.draw()