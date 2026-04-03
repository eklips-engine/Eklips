## Import libraries & components
from .transform        import Transform
from typing            import *
from classes.locals    import *
from typing_extensions import *

## Classes
class Mouse(Transform):
    #: Relative pos from last frame
    dpos         = [0,0]
    #: If mouse is dragging
    dragging     = False
    #: 1 is up, -1 is down
    scroll       = 0
    #: Buttons just now pressed. Use `engine.is_action_pressed` instead.
    just_clicked = MOUSE_DEFAULT_STATE.copy()
    #: Use `engine.is_action_pressed` instead.
    buttons      = MOUSE_DEFAULT_STATE.copy()
    #: List of filepaths
    paths        = []
class Keyboard:
    #: Keyboard modifiers.
    modifiers = 0
    #: Dictionary of keys pressed. Use `engine.is_action_pressed` instead.
    pressed   = {}
    #: Dictionary of keys held down. Use `engine.is_action_pressed` instead.
    held      = {}
    #: Text from Window.on_text.
    text      = ""
    #: Motion from Window.on_text_motion.
    motion    = None
