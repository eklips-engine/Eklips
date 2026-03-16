# Import libraries
import pyglet as pg
from classes.nodes.gui.colorrect import *

# Classes
class Inputbox(ColorRect, Color):
    """
    An inputbox element.
    
    XXX
    """
    _blinktimer = 0.5
    
    ## Exports
    @export("", "str", "str")
    def value(self):
        return self._value
    @value.setter
    def value(self, val):
        self._value     = val
    
    ## Transform related
    def _set_alpha(self, deg):
        self.citem.alpha = deg
        self.label.alpha = deg
    def _set_visible(self, val):
        self.citem.visible = val
        self.label.visible = val
    
    ## Init
    def __init__(self, properties={}, parent=None):
        # Setup CanvasItem
        Color.__init__(self, *WHITE)
        super().__init__(properties, parent)
        
        # Alias
        self.widgetman = engine.scene._widgetman
        
        # Set properties
        self._value   = ""
        self._elapsed = 0
        self.gid      = self.widgetman.add_widget(self)

        # Make new item
        self._make_new_item()
    
    ## CItem management
    def _fix_broken_item(self):
        self._remove_item(False)
        del self._cached_batch
        self._make_new_item()
        self._convert_transform_property_into_object(self.transform)
    def _make_new_item(self):
        if self.citem:
            self._remove_item(False)
        else:
            self._drawing_bid = self.viewport.add_batch()

        self.citem = pg.shapes.Rectangle(0,0,self.w,self.h, color=self.color, batch=self.batch)
        self.label = pg.text.Label(
            text   = self.value,
            batch  = self.batch)
        self._set_anchors()
    def _remove_item(self, remove_batches=True):
        self.citem.delete()
        self.label.delete()
        if self.viewport and remove_batches:
            self.viewport.batches.pop(self.batch_id)
    
    def update(self):
        super().update()
        
        ## Focusing
        if self.get_if_mouse_hovering():
            self.widgetman.hovering_widget = self.gid
        else:
            if self.widgetman.hovering_widget == self.gid:
                self.widgetman.hovering_widget = -1

        if engine.mouse.buttons[MOUSE_LEFT]:
            if self.widgetman.hovering_widget == self.gid:
                self.widgetman.focused_widget  = self.gid

        ## Mouse
        if self.widgetman.hovering_widget == -1:
            engine.set_mouse(MOUSE_NORMAL, self.window_id)
        if self.get_if_mouse_hovering():# or self.widgetman.focused_widget == self.gid:
            engine.set_mouse(MOUSE_IBEAM, self.window_id)
            self.widgetman.moving_widget = -1

        ## Typing
        if self.widgetman.focused_widget == self.gid:
            char = engine.keyboard.text
            key  = None

            for kid in engine.keyboard.pressed:
                if engine.keyboard.pressed[kid] and not key:
                    key = kid
            
            if char != "":
                self.value += char
            elif key == pg.window.key.ENTER:
                self.widgetman.focused_widget = -1
            elif key == pg.window.key.BACKSPACE:
                self.value = self.value[:-1]
            elif key == pg.window.key.CLEAR:
                self.value = " "
        
        ## Draw it
        self._elapsed += engine.delta
        if self._elapsed  > self._blinktimer*2:
            self._elapsed = 0
        self.draw()
        
    def _free(self):
        self.widgetman.widgets.pop(self.gid)
        super()._free()
    
    def draw(self):
        ## Check if visible
        if not (self.visible and self.viewport.is_onscreen(self)):
            return
        
        ## Get position of full object
        x,   y = self.into_screen_coords()
        tx, ty = self.into_screen_coords(drawing=True)

        ## Move bg
        self.citem.x = tx
        self.citem.y = ty

        ## Move label
        self.label.x = x + 5
        self.label.y = y + self.h / 2 - self.label.content_height / 2 + 5

        self.label.text = f"{self.value}{'_' if self._elapsed > self._blinktimer and self.widgetman.focused_widget == self.gid else ' '}"