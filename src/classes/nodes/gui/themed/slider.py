# XXX
# Import libraries
import pyglet as pg
from classes import ui

# Import inherited
from classes.nodes.gui.canvasitem import *

# Classes
class Slider(CanvasItem):
    """
    A slider element.
    
    XXX
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
    
    @value.setter
    def value(self, val):
        print(val, "b")
        if val  < self.minimum:
            val = self.minimum
        if val  > self.maximum:
            val = self.maximum
        self._value   = val
        print(val, "a")
    @minimum.setter
    def minimum(self, val):
        self._minimum = val
    @maximum.setter
    def maximum(self, val):
        self._maximum = val
    
    def _set_size(self, w, h):
        self._stf.scale_x = w / self.slider_bg.image.width
        self._stf.scale_y = (h-20) / self.slider_bg.image.height
        super()._set_size(w, h)
    
    def __init__(self, properties={}, parent=None):
        # Setup CanvasItem
        super().__init__(properties, parent)
        
        # Alias
        self.widgetman = engine.scene._widgetman
        
        # Set properties
        self._minimum = 0
        self._maximum = 150
        self._value   = 0
        self.gid      = self.widgetman.add_widget(self)
        
        # Make item
        self._make_new_item()
        self._stf = Transform() # Slider BG Transform
        self._ktf = Transform() # Knob transform
        
    
    def _make_new_item(self):
        self.slider_bg = pg.sprite.Sprite(
            img        = engine.theme.get_static_widget("bg"),
            batch      = self.viewport.batches[self.batch_id])
        self.knob      = pg.sprite.Sprite(
            img        = engine.theme.get_static_widget("knob"),
            batch      = self.viewport.batches[self.batch_id])
    
    def _remove_item(self):
        self.slider_bg.delete()
        self.knob.delete()
    
    def get_if_mouse_hovering_knob(self) -> bool:
        """Returns true if the mouse is hovering over the knob."""
        if not self.viewport:
            return
        mpos   = engine.mouse.pos
        x,  y  = self._ktf.into_screen_coords(self.viewport.tsize)
        vx, vy = self.viewport.into_screen_coords()
        is_it  = (
            mpos[0] >= ((x + vx - self.viewport.cam.x) * self.viewport.cam.zoom)                                          and
            mpos[0] <= ((x + vx - self.viewport.cam.x) * self.viewport.cam.zoom) + (self._ktf.w * self.viewport.cam.zoom) and
            mpos[1] >= ((y + vy - self.viewport.cam.y) * self.viewport.cam.zoom)                                          and
            mpos[1] <= ((y + vy - self.viewport.cam.y) * self.viewport.cam.zoom) + (self._ktf.h * self.viewport.cam.zoom)
        )
            
        return is_it
    
    def update(self):
        super().update()
        
        if engine.mouse.buttons[MOUSE_LEFT]:
            if self.get_if_mouse_hovering_knob():
                if self.widgetman.moving_widget == -1:
                    self.widgetman.focused_widget = self.gid
                if engine.mouse.dragging and self.widgetman.focused_widget == self.gid:
                    self.widgetman.moving_widget  = self.gid
            if self.widgetman.moving_widget  == self.gid:
                x, y        = self.into_screen_coords(self.viewport.tsize)
                self.value += (engine.mouse.dpos[0])/self.w*self.maximum
        else:
            if self.get_if_mouse_hovering_knob() or self.widgetman.moving_widget == self.gid:
                self.widgetman.moving_widget = -1
        self.draw()
        
    def _free(self):
        self.widgetman.widgets.pop(self.gid)
        super()._free()
    
    def _draw(self):
        x, y = self.into_screen_coords(self.viewport.tsize)
        
        self._stf.x = x + 5
        self._stf.y = y + 5
        self._ktf.y = y
        
        if self._value  == 0:
            self._ktf.x = x
        else:
            self._ktf.x = x + (self._value/self._maximum)*self.w
        
        engine.display.blit(
            transform   = self._stf,
            window_id   = self.window_id,
            viewport_id = self.viewport_id,
            sprite      = self.slider_bg
        )
        engine.display.blit(
            transform   = self._ktf,
            window_id   = self.window_id,
            viewport_id = self.viewport_id,
            sprite      = self.knob
        )