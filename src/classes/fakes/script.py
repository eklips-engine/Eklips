from classes.customprops import export

class _ScriptDoc:
    _runnable        = True
    _script_path     = None
    _script          = None
    _can_init_script = True
    obj_id           = None
    file_path        = None
    source_code      = "# Empty.. Please initialize the Script in your Object."
    _can_init_script = False
    _namespace       = {}
    _function_queue  = []
    @property
    def script(self): ...
    @export(None,"str","file_path/ekl")
    def script_path(self) -> str:
        pass
    
    @script.setter
    def script(self): ...
    @script_path.setter
    def script_path(self, path : str): ...
    def __init__(self): ...
    def get_class_name(self) -> str: 
        """Return the name of the Object. (e.g. Object, Node...)"""
    def _free(self): ...
    def free(self):
        """Free the object from memory."""
    def get(self, name, fallback=None):
        """Get the Object property `name`, if non-existent, return `fallback`."""
    def set(self, name, value):
        """Set the Object property `name` into `value`."""
    def call(self, function, *args):
        """Call a function from the attached Script, if it exists."""
    def call_signal(self, signal_name, *args):
        """Call an attached signal from the attached Script, if it exists."""
    def call_deferred(self, function, *args, is_signal = False) -> None:
        """Call a function/signal from the attached Script after the Script has finished its process tick."""
    def _process(self):
        """Run the `_process()` function on the Script. This is called every frame of the Object/Node's existence."""
    def _onready(self):
        """Run the `_onready()` function on the Script. This should only be called after the Object/Node is ready."""    

