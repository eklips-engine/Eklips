## Import libraries & components
import json
from typing            import *
from classes.locals    import *
from typing_extensions import *

## Classes
class WindowProperties:
    """Properties for the main Window."""
    maxsize      : list = [0,0]
    minsize      : list = [0,0]
    color        : list = BLACK
    resizable    : bool = False
    antialiasing : bool = False
    vsize        : list = [0,0]
    icofile      : str  = ""
class DebugConfig:
    """Debugging configuration."""
    _skipload  = False
    _freezload = False
    _enabled   = True
    _showfps   = True
    _nomercy   = False
    _alwaysvis = False

    @property
    def sprite_always_visible(self):
        """True if sprites are always visible. Read-write."""
        return self._alwaysvis and self._enabled
    @sprite_always_visible.setter
    def sprite_always_visible(self,val): self._alwaysvis = val

    @property
    def skip_load(self):
        """True if the loading animation can be skipped. Read-write."""
        return self._skipload and self._enabled
    @skip_load.setter
    def skip_load(self,val): self._skipload = val

    @property
    def freeze_load(self):
        """True if the loading animation can be frozen. Read-write."""
        return self._freezload and self._enabled
    @freeze_load.setter
    def freeze_load(self,val): self._freezload = val

    @property
    def show_fps(self):
        """True if the engine can show the FPS. Read-write."""
        return self._showfps and self._enabled
    @show_fps.setter
    def show_fps(self,val): self._showfps = val

    @property
    def avoid_error_mercy(self):
        """True if the engine can be more error-prone. Read-write."""
        return self._nomercy and self._enabled
    @avoid_error_mercy.setter
    def avoid_error_mercy(self,val): self._nomercy = val

    @property
    def enabled(self):
        """True if debugging is enabled. Read-write."""
        return self._enabled
    @enabled.setter
    def enabled(self,val): self._enabled = val
class GameData:
    """Data about the running project."""
    
    #: The location of the game.json file being used.
    project_file = None
    #: The directory of the project that is running.
    project_dir  = None

    #: The project's version.
    version     = None
    #: The project's Eklips version.
    version_ekl = None
    
    #: The save folder.
    save_dir = None

    #: Main Window properties
    win = None

    #: List of fonts
    fonts = None

    #: The directory of all of the language files.
    langdir = None
    #: List of languages.
    langs   = None

    #: Dictionary of actions.
    actions = None

    #: The main scene.
    master_scene  = None
    #: The scene loaded at the start of the runtime. Can be used for a loading animation, etc..
    loading_scene = None

    def __init__(self, settings="settings.json", is_file = True):
        ### Settings file related
        ## Load settings
        if is_file:
            self.file_data = json.loads(open(settings).read())
        else:
            self.file_data = settings

        ### Get data about what project to use
        self.metadata     = self.file_data["project"]

        ## Get project itself
        self.project_file = str(self.metadata["file"]).replace("\\", "/")
        self.project_dir  = self.metadata["dir"].replace("\\", "/")
        
        # Check if arguments decide otherwise ("-file ...", "-dir ...")
        words = sys.argv
        wrid  = 0
        for current in words:
            try:
                after  = words[wrid+1]
                before = words[wrid-1]
            except:
                after  = None
                before = None
            
            if current.startswith("-"):
                if after == None:
                    wrid += 1
                elif current == "-dir":
                    self.project_dir  = after.replace("\\", "/")
                elif current == "-file":
                    self.project_file = after.replace("\\", "/")
                
            wrid += 1

        if self.project_dir == USE_GAME_PARENT:
            self.project_dir = "/".join(self.project_file.split("/")[:-1])
        
        if os.path.isfile(self.project_file):
            self.project_data = json.loads(open(self.project_file).read())
        else:
            self.project_data = json.loads(open("_assets/no_game/game.json").read())
            self.project_dir  = "_assets/no_game"

        #### Project file related
        # Get basic metadata
        self.name        = self.project_data["name"]
        self.version     = self.project_data["version"]["app"]
        self.version_ekl = self.project_data["version"]["ekl"]
        
        # Make save directory
        self.save_dir    = f"{pg.resource.get_data_path("Eklips Engine")}/{self.name}"
        os.makedirs(self.save_dir, exist_ok=True)

        # Initialize window properties
        self.win              = WindowProperties()
        self.win.vsize        = self.project_data["viewport"]["size"]
        self.win.color        = self.project_data["viewport"]["color"]
        self.win.resizable    = self.project_data["viewport"]["resizable"]
        self.win.minsize      = self.project_data["viewport"]["minsize"]
        self.win.maxsize      = self.project_data["viewport"]["maxsize"]
        self.win.icofile      = self.project_data["viewport"]["icon_file"]
        self.win.antialiasing = self.project_data["behavior"]["antialiasing"]

        # Text-related
        self.fonts   = self.project_data["behavior"]["fonts"]
        self.langs   = self.project_data["language"]["langs"]
        self.langdir = self.project_data["language"]["dir"]
        self.actions = self.project_data["actions"]

        # Get scenes info
        self.master_scene  = self.project_data["scenes"]["master"]
        self.loading_scene = self.project_data["scenes"]["loading"]