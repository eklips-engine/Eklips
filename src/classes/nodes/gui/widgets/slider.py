## Import libraries
import pyglet as pg
from classes.nodes.gui.canvasitem import *

## Classes
class Slider(CanvasItem):
    """
    A themed slider element.
    """
    
    @export(0, "int", "int")
    def value(self):
        return self._value
    @export(0, "int", "int")
    def minimum(self):
        return self._minimum
    @export(150, "int", "int")
    def maximum(self):
        return self._maximum
    @export(True, "bool", "bool")
    def show_percentage(self):
        return self._showpercent
    
    @value.setter
    def value(self, val):
        if val  < self.minimum:
            val = self.minimum
        if val  > self.maximum:
            val = self.maximum
        self._value   = val
    @minimum.setter
    def minimum(self, val):
        self._minimum = val
    @maximum.setter
    def maximum(self, val):
        self._maximum = val
    @show_percentage.setter
    def show_percentage(self, val):
        self._showpercent = val
    
    def _set_size(self, w, h):
        self.slider_bg.scale_x = w      / self.slider_bg.image.width
        self.slider_bg.scale_y = (h-20) / self.slider_bg.image.height
    def _set_scale(self, x, y):
        self._set_size()
    def _set_flip(self, w, h):
        return
    def _set_alpha(self, deg):
        self.citem.alpha = deg
        self.slider_bg.alpha = deg
        self.label.alpha = deg
    def _set_rot(self, deg):
        self.citem.rotation = deg
    def _set_visible(self, val):
        self.citem.visible = val
        self.slider_bg.visible = val
        self.label.visible = val
    
    def __init__(self, properties={}, parent=None):
        # Setup CanvasItem
        super().__init__(properties, parent)
        
        # Alias
        self.widgetman = engine.scene._widgetman
        
        # Set properties
        self._knobtf   = Transform()
        self.slider_bg = None
        self.label     = None

        self._showpercent = True
        self._minimum     = 0
        self._maximum     = 150
        self._value       = 0
        self.gid          = self.widgetman.add_widget(self)

        # Make new item
        self._make_new_item()
    
    ## CItem Management
    def _refresh_item(self):
        if self.citem:
            self._remove_item(False)
            del self._cached_batch
        self._make_new_item()
    def _make_new_item(self):
        if self.slider_bg:
            self._remove_item(False)
        else:
            self._drawing_bid = self.viewport.add_batch()
            if getattr(self, "_cached_batch", None):
                del self._cached_batch
        
        self.slider_bg = pg.sprite.Sprite(
            img        = engine.theme.get_static_widget("bg"),
            batch      = self.batch)
        self.citem      = pg.sprite.Sprite(
            img        = engine.theme.get_static_widget("knob"),
            batch      = self.batch)
        self.label     = pg.text.Label(
            text       = f"0%",
            batch      = self.batch)
        
        self._knobtf.w = self.citem.image.width
        self._knobtf.h = self.citem.image.width
        self._set_size(*self.size)
        self._set_anchors()
    def _set_anchors(self):
        self.slider_bg.image.anchor_x = self.slider_bg.image.width  // 2
        self.slider_bg.image.anchor_y = self.slider_bg.image.height // 2
        self.citem.image.anchor_x     = self.citem.image.width      // 2
        self.citem.image.anchor_y     = self.citem.image.height     // 2
        self.citem._update_position()
    def _remove_item(self, remove_batches=True):
        if not self.slider_bg or not self.slider_bg._vertex_list:
            return
        self._switch_window()
        self.slider_bg.delete()
        self.citem.delete()
        self.label.delete()
        if self.viewport and remove_batches:
            self.viewport.batches.pop(self.batch_id)
    
    def get_if_mouse_hovering(self) -> bool:
        """Returns true if the mouse is hovering over the knob."""
        if not self.viewport:
            return
        if not self.viewport.is_onscreen(self):
            return

        ## Result
        return self.mouse.collides_ui_aabb(self._knobtf,
            ctx_a=(self.viewport, self._isc_get_parent_property(), 0),
            ctx_b=(self._get_window(), None, 0))
    
    def update(self):
        super().update()
        
        ## Handle knob
        if self.get_if_mouse_hovering():
            self.widgetman.hovering_widget = self.gid
        else:
            if self.widgetman.hovering_widget == self.gid:
                self.widgetman.hovering_widget = -1

        if self.mouse.buttons[MOUSE_LEFT]:
            if self.get_if_mouse_hovering():
                if self.widgetman.moving_widget == -1:
                    self.widgetman.focused_widget = self.gid
                if self.mouse.dragging and self.widgetman.focused_widget == self.gid:
                    self.widgetman.moving_widget  = self.gid
            if self.widgetman.moving_widget  == self.gid:
                engine.set_mouse(MOUSE_DRAG, self.window_id)
                self.value += (self.mouse.dpos[0])/self.w*self.maximum
        else:
            if self.widgetman.hovering_widget == -1:
                engine.set_mouse(MOUSE_NORMAL, self.window_id)
            if self.get_if_mouse_hovering() or self.widgetman.moving_widget == self.gid:
                engine.set_mouse(MOUSE_DRAGGABLE, self.window_id)
                self.widgetman.moving_widget  = -1
                self.widgetman.focused_widget = -1
        
        ## Draw it
        self.draw()
        
    def _free(self):
        self.widgetman.widgets.pop(self.gid)
        super()._free()
    
    def draw(self):
        ## Check if visible
        if not (self.visible and self.viewport.is_onscreen(self)):
            return
        
        ## Fun little feature
        self.citem.rotation = self._knobtf.rotation = self.value/self.maximum*360

        ## Set label text
        self.label.text = f"{int(self.value/self.maximum*100)}%" if self.show_percentage else f"{int(self.value)}"
        
        ## Get position of full slider object
        bgx, bgy = self.into_viewport_coords(drawing=True)
        x,     y = self.into_viewport_coords()

        ## Move bg
        self.slider_bg.x = bgx + 5
        self.slider_bg.y = bgy - 5

        ## Move label
        self.label.x = x + self.w / 2 - self.label.content_width  / 2
        self.label.y = y + self.h / 2 - self.label.content_height / 2

        ## Move knob
        self.citem.y   = y + self.citem.height / 2
        self._knobtf.y = self.viewport.h-self.citem.height - self.citem.y 
        if self._value   == 0:
            self.citem.x = x
        else:
            self.citem.x = x + ((self._value+ZDE_FIX)/self._maximum*self.w)
        self._knobtf.x = self.citem.x
        self.citem.x  += self.citem.image.anchor_x