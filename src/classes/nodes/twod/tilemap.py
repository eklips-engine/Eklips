# Import libraries
from classes.resources.tileset    import *
from classes.nodes.gui.canvasitem import *

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
        self._tiles = {}
        self._tileset: Tileset = None
        self._latestid = 0

        self._vertices  = []
        self._texcoords = []
        self._count     = 0

        super().__init__(properties, parent)
        self._make_new_item()

    ## VertexList management
    def _make_new_item(self):
        if self.citem:
            self.citem.delete()

        self._drawing_bid  = self.viewport.add_batch()
        self._cached_batch = self.viewport.batches[self.batch_id]

        self._vertices.clear()
        self._texcoords.clear()
        self._count = 0

        self._build()
    def _build(self):
        if not self.tileset or not self.tiles:
            self.citem = None
            return

        tex = self.tileset.texture.get_texture()

        for tid in self.tiles:
            self._append_tile(tid)

        tex.bind()
        self._program = pg.graphics.get_default_shader()
        self.citem    = self._program.vertex_list(
            self._count,
            pg.gl.GL_QUADS,
            #batch=self.batch,
            position=("f", self._vertices),
            tex_coords=("f", self._texcoords),
            texture=tex
        )

    def _append_tile(self, tid):
        tile = self._tiles[tid]

        gx, gy = tile["position"]
        tw, th = self.tileset.grid_size

        x = gx * tw
        y = gy * th

        self._vertices += [
            x,     y, 0,
            x+tw,  y, 0,
            x+tw,  y+th, 0,
            x,     y+th, 0
        ]

        self._texcoords += self.tileset.get_uv(tile["tile"])
        self._count     += 4
    def _rebuild(self):
        self._make_new_item()

    ## Tile management
    def place_tile(self, tid, x, y):
        _id = self._latestid

        self._tiles[_id] = {
            "tile": tid,
            "position": [x, y]
        }

        self._latestid += 1
        self._append_tile(_id)
        return _id
    def remove_tile(self, tid):
        if tid in self._tiles:
            self._tiles.pop(tid)
            self._rebuild()

    ## Draw related
    def draw(self):
        if not self.visible or not self.citem:
            return

        tex = self.tileset.texture.get_texture()
        tex.bind()

        x, y = self.into_screen_coords(do_flip=False)

        self.citem.draw(pg.gl.GL_QUADS)

        """
        map_x, map_y = self.into_screen_coords(do_flip=False)
        verts        = self.citem.position
        
        tw, th = self.tileset.grid_size
        sx, sy = self.scale_x, self.scale_y

        i = 0
        for tid in self._tiles:
            gx, gy = self._tiles[tid]["position"]

            x = map_x + gx * tw * sx
            y = map_y + gy * th * sy
            w = tw * sx
            h = th * sy

            verts[i:i+12] = [
                x,   y,   0,
                x+w, y,   0,
                x+w, y+h, 0,
                x,   y+h, 0
            ]
            i += 12
        """

    def update(self):
        super().update()
        self.draw()