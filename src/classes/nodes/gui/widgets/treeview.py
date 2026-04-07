## XXX implement the rendering part
## Import libraries
import pyglet as pg
from classes import ui
from functools import reduce
import operator

## Import inherited
from classes.nodes.gui.canvasitem import *

class Treeview(CanvasItem):
    ## Init
    def __init__(self, properties={}, parent=None):
        self._items = {}
        super().__init__(properties, parent)
    
    ## Export
    @export({}, "dict", "treeview/children")
    def items(self) -> dict:
        return self._items
    @items.setter
    def items(self, val):
        # format is:
        ## Item: { child1: {}, child2: {child1: {}} ... }
        self._items = val
    
    ## Update
    def update(self):
        # Draw Treeview
        for item in self.items:
            ...

        # Update CanvasItem
        super().update()

    ## Item management
    def _navigate_to_item(self, path, create_path=False):
        """Navigate to an item in the tree. Returns (parent_dict, final_key) or (None, None) if not found."""
        try:
            keys = path.split('/')
            d = self._items
            for k in keys[:-1]:
                if create_path:
                    d = d.setdefault(k, {})
                else:
                    d = d[k]
            return d, keys[-1]
        except:
            return None
    def add_item(self, path, name):
        d, key = self._navigate_to_item(path, create_path=True)
        if d is not None:
            d[key] = [name, False]
            return 0
        return 1
    def open(self, path):
        d, key = self._navigate_to_item(path, create_path=False)
        if d is not None and isinstance(d.get(key), list) and len(d[key]) > 1:
            d[key][1] = True
            return 0
        return 1
    def close(self, path):
        d, key = self._navigate_to_item(path, create_path=False)
        if d is not None and isinstance(d.get(key), list) and len(d[key]) > 1:
            d[key][1] = False
            return 0
        return 1