## Import inherited
from classes.nodes.gui.extraviewport import *
from classes.ui                      import *

## Classes
class ScrollingViewport(ExtraViewport):
    """
    A Viewport Node.
    
    This Node will create a new Viewport. You can get this Viewport
    by using `engine.display.get_viewport(node.viewport_id, wid)`
    or by using `node` itself.

    You can use the scroll wheel on the mouse to move the Viewport's
    contents (or rather Camera, but that doesn't sound so magical
    now, does it?), or use the scrollbar instead.
    """
    _isdisplayobject = True

    @export(300.0,"float","slider")
    def speed(self):
        """How fast the scrolling should be.

        The reason why the default value is so high
        because on 1x speed, it takes 1 second to
        move 1 pixel.

        You can make this value negative to go backwards.
        """
        return self._speed
    @speed.setter
    def speed(self, value):
        self._speed = value

    @export(False, "bool", "bool")
    def left_to_right(self):
        return self._left_to_right
    @left_to_right.setter
    def left_to_right(self, value):
        self._left_to_right = value
        if value:
            self.scrollbar_bg.image = engine.theme.get_static_widget("scrollbg_hor")
        else:
            self.scrollbar_bg.image = engine.theme.get_static_widget("scrollbg")
        self._set_scrollbar_size()
    
    @export(False, "int", "slider")
    def content_width(self):
        return self._content_width
    @content_width.setter
    def content_width(self, value):
        if value < ZDE_FIX: value = ZDE_FIX
        self._content_width = value
    
    @export(False, "int", "slider")
    def content_height(self):
        return self._content_height
    @content_height.setter
    def content_height(self, value):
        if value < ZDE_FIX: value = ZDE_FIX
        self._content_height = value
    
    def _set_scrollbar_size(self):
        if self.left_to_right:
            self.scrollbar_bg.scale_x = self._w               / self.scrollbar_bg.image.width
            self.scrollbar_bg.scale_y = self.scrollbar.height / self.scrollbar_bg.image.height
        else:
            self.scrollbar_bg.scale_x = self.scrollbar.width / self.scrollbar_bg.image.width
            self.scrollbar_bg.scale_y = self._h              / self.scrollbar_bg.image.height
    def _set_size(self, w, h):
        self._set_scrollbar_size()
        super()._set_size(w, h)
    
    def __init__(self, properties={}, parent=None):
        # Setup vp
        super().__init__(properties, parent)
        
        # Add batch for scrollbar
        self._scrollbarbatch = self.add_batch()

        # Setup UI
        self._scrollbartf                    = Transform()
        self.scrollbar    : pg.sprite.Sprite = None
        self.scrollbar_bg : pg.sprite.Sprite = None
        self._make_ui_elements()
        
        # Alias
        self.widgetman = engine.scene._widgetman

        # Set properties
        self._content_height = 720
        self._content_width  = 1280
        self._speed          = 180
        self._left_to_right  = False
        self.gid             = self.widgetman.add_widget(self)
        
    def _make_new_item(self):
        self._make_framebuffer()
        self._make_ui_elements()
    def _refresh(self):
        super()._refresh()

        ## Remake UI elements
        self._remove_ui_elements()
        self._make_ui_elements()
    def _remove_ui_elements(self):
        if self.scrollbar_bg:
            self.scrollbar_bg.delete()
            self.scrollbar.delete()
        self.scrollbar_bg = None
        self.scrollbar    = None
    def _remove_item(self):
        super()._remove_item()
        self._remove_ui_elements()
    def _make_ui_elements(self):
        self.scrollbar_bg = pg.sprite.Sprite(
            img   = engine.theme.get_static_widget("scrollbg"),
            batch = self.batches[self._scrollbarbatch])
        self.scrollbar    = pg.sprite.Sprite(
            img   = engine.theme.get_static_widget("scrollbtn"),
            batch = self.batches[self._scrollbarbatch])
        
        self._scrollbartf.w = self.scrollbar.image.width
        self._scrollbartf.h = self.scrollbar.image.height
    def _free(self):
        self.widgetman.widgets.pop(self.gid)
        super()._free()
    
    def get_if_mouse_hovering_knob(self) -> bool:
        """Returns true if the mouse is hovering over the knob."""

        ## Result
        return self.mouse.collides_ui_aabb(self._scrollbartf,
            ctx_a=(self, self._isc_get_parent_property(), 1),
            ctx_b=(self._get_window(), None, 1))
    
    ## Update loop
    def update(self):
        super().update()

        # Check if not wasting time
        if not self.visible:
            self.scrollbar.visible    = False
            self.scrollbar_bg.visible = False
            return
        elif self.content_height     == ZDE_FIX or self.content_width == ZDE_FIX:
            self.scrollbar.visible    = False
            self.scrollbar_bg.visible = False
            return
        else:
            self.scrollbar.visible    = True
            self.scrollbar_bg.visible = True
        
        # Handle the knob
        hovering_knob = self.get_if_mouse_hovering_knob()
        if hovering_knob:
            self.widgetman.hovering_widget = self.gid
        else:
            if self.widgetman.hovering_widget == self.gid:
                self.widgetman.hovering_widget = -1
        
        if self.mouse.buttons[MOUSE_LEFT]:
            if hovering_knob:
                if self.widgetman.moving_widget  == -1:
                    self.widgetman.focused_widget = self.gid
                if self.mouse.dragging and self.widgetman.focused_widget == self.gid:
                    self.widgetman.moving_widget  = self.gid
            if self.widgetman.moving_widget      == self.gid:
                self._vel = 0
                engine.set_mouse(MOUSE_DRAG, self.window_id)
                if self._left_to_right:
                    self.cam.x    += self.mouse.dpos[0] / (self._w-self.scrollbar.width) * self.content_width
                    if self.cam.x  < 0:
                        self.cam.x = 0
                else:
                    self.cam.y    += self.mouse.dpos[1] / (self._h-self.scrollbar.height) * self.content_height
                    if self.cam.y  > 0:
                        self.cam.y = 0
        else:
            if self.widgetman.hovering_widget == -1:
                engine.set_mouse(MOUSE_NORMAL, self.window_id)
            if hovering_knob or self.widgetman.moving_widget == self.gid:
                engine.set_mouse(MOUSE_DRAGGABLE, self.window_id)
                self.widgetman.moving_widget = -1
        
        # Handle spinning the mouse wheel
        vel = 0
        if self.mouse.scroll != 0 and self.get_if_mouse_hovering():
            vel = self.mouse.scroll * self.speed
        
        # Camera and scrollbar sprite handling
        if self._left_to_right:
            self.cam.x   -= vel * engine.delta
            if self.cam.x  < 0:
                self.cam.x = 0
            if self.cam.x > self.content_width:
                self.cam.x = self.content_width
        else:
            self.cam.y   += vel * engine.delta
            if self.cam.y  > 0:
                self.cam.y = 0
            if self.cam.y < -self.content_height:
                self.cam.y = -self.content_height

        # Draw it
        self.draw()
    def draw(self):
        ## Draw scrollbar
        if self._left_to_right:
            self.scrollbar_bg.x = self.cam.x
            self._scrollbartf.y = self._h-self.scrollbar.height+(self.scrollbar.height*2)
            self.scrollbar_bg.y = self.scrollbar.y = 0

            x                   = ((self.cam.x/self.content_width) * (self._w-self.scrollbar.width))
            self.scrollbar.x    = self.cam.x + x
            self._scrollbartf.x = abs(x)
        else:
            self.scrollbar_bg.y = self.cam.y
            self.scrollbar_bg.x = self._w-self.scrollbar_bg.width
            self.scrollbar.x    = self._scrollbartf.x = self._w-self.scrollbar.width

            y                   = (self.cam.y/self.content_height) * (self._h-self.scrollbar.height)
            self._scrollbartf.y = abs(y)+(self.scrollbar.height*2)
            self.scrollbar.y    = self._h-self.scrollbar.height + self.cam.y+y
        
        ## Then VP
        super().draw()