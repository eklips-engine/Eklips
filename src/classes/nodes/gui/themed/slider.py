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
        self._stf.scale_x = w / self.slider_bg.image.width
        self._stf.scale_y = (h-20) / self.slider_bg.image.height
    def _set_alpha(self, deg):
        self._ktf.alpha = deg
        self._stf.alpha = deg
        self._ltf.alpha = deg
    def _set_rot(self, deg):
        self._ktf.rotation = deg
    def _set_visible(self, val):
        self._ktf.visible = val
        self._stf.visible = val
        self._ltf.visible = val
    
    def __init__(self, properties={}, parent=None):
        # Setup CanvasItem
        super().__init__(properties, parent)
        
        # Alias
        self.widgetman = engine.scene._widgetman
        
        # Set properties
        self._showpercent = True
        self._minimum     = 0
        self._maximum     = 150
        self._value       = 0
        self.gid          = self.widgetman.add_widget(self)
        
        # Make item
        self._make_new_item()
        self._stf = Transform() # Slider BG Transform
        self._ktf = Transform() # Knob transform
        self._ltf = Transform() # Label transform
    
    def _make_new_item(self):
        self._drawing_bid = self.viewport.add_batch()
        self.slider_bg    = pg.sprite.Sprite(
            img           = engine.theme.get_static_widget("bg"),
            batch         = self.viewport.batches[self.batch_id])
        self.knob         = pg.sprite.Sprite(
            img           = engine.theme.get_static_widget("knob"),
            batch         = self.viewport.batches[self.batch_id])
        self.label        = pg.text.Label(
            text          = f"?%",
            batch         = self.viewport.batches[self.batch_id])
    
    def _remove_item(self):
        self.slider_bg.delete()
        self.knob.delete()
        if self.viewport:
            self.viewport.batches.pop(self.batch_id)
    
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
        
        ## Handle knob
        if self.get_if_mouse_hovering_knob():
            self.widgetman.hovering_widget = self.gid
        else:
            if self.widgetman.hovering_widget == self.gid:
                self.widgetman.hovering_widget = -1

        if engine.mouse.buttons[MOUSE_LEFT]:
            if self.get_if_mouse_hovering_knob():
                if self.widgetman.moving_widget == -1:
                    self.widgetman.focused_widget = self.gid
                if engine.mouse.dragging and self.widgetman.focused_widget == self.gid:
                    self.widgetman.moving_widget  = self.gid
            if self.widgetman.moving_widget  == self.gid:
                engine.set_mouse(MOUSE_DRAG)
                x, y        = self.into_screen_coords(self.viewport.tsize)
                self.value += (engine.mouse.dpos[0])/self.w*self.maximum
        else:
            if self.widgetman.hovering_widget == -1:
                engine.set_mouse(MOUSE_NORMAL)
            if self.get_if_mouse_hovering_knob() or self.widgetman.moving_widget == self.gid:
                engine.set_mouse(MOUSE_DRAGGABLE)
                self.widgetman.moving_widget = -1
        
        ## Draw it
        self.draw()
        
    def _free(self):
        self.widgetman.widgets.pop(self.gid)
        super()._free()
    
    def draw(self):
        x, y = self.into_screen_coords(self.viewport.tsize)
        
        self._stf.x = x + 5
        self._stf.y = y + 5
        self._ktf.y = y
        self._ltf.y = y + self.h / 2 - self._ltf.h / 2
        self._ltf.x = x + self.w / 2 - self._ltf.w / 2
        
        if self._value  == 0:
            self._ktf.x = x - self.knob.width/2
        else:
            self._ktf.x = x + (self._value/self._maximum)*self.w - self.knob.width/2
        
        self.viewport.blit_sprite(self._stf,self.slider_bg)
        self.viewport.blit_sprite(self._ktf,self.knob)
        self.viewport.blit_label(
            text        = f"{int(self.value/self.maximum*100)}%" if self.show_percentage else f"{int(self.value)}",
            transform   = self._ltf,
            label       = self.label
        )