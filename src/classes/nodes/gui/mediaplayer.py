## Import libraries
from classes.nodes.gui.canvasitem import *
from classes.resources            import MediaFile

## Classes
class MediaPlayer(CanvasItem):
    """
    A Media Player.

    This is a Node that can play video and audio globally.
    """
    _audiofile   = None
    
    def __init__(self, properties={}, parent=None):
        self._media       : str          = ""
        self._playcounter : int          = 0
        self._rpop        : bool         = True
        self._playing     : bool         = False
        self._volume      : float | int  = 0
        self._media       : MediaFile    = MediaFile()
        self._autostart   : bool         = False
        self._loops       : int          = 0

        self._make_new_item()
        self.citem.visible = False
        super().__init__(properties, parent)
    
    def _setup_properties(self, scene=None):
        super()._setup_properties(scene)
        if self.auto_start:
            self.play()
    
    ## Exports
    @export(1.0, "float", "float")
    def volume(self) -> int:
        """Volume of the attached Media file."""
        return self._volume
    @volume.setter
    def volume(self, value : int | float | None):
        self._volume       = value
        self._media.volume = value
    @export(False, "bool", "bool")
    def auto_start(self):
        """If the Media should automatically start when created."""
        return self._autostart
    @auto_start.setter
    def auto_start(self, value):
        self._autostart = value
    @export(0,     "int",   "int")
    def loops(self) -> int:
        """How many times the Media should loop. Set to a value less than 0 for infinite."""
        return self._loops
    @loops.setter
    def loops(self, value): self._loops = value
    @export(True, "bool",  "bool")
    def reset_playback_on_play(self) -> bool:
        """If the playback should restart if the `play()` function is called.

        If False, `play()` will stop if `busy` is true.
        If True, the playback will restart. This may lead to noise if `play()` is spammed."""
        return self._rpop
    @reset_playback_on_play.setter
    def reset_playback_on_play(self, value): self._rpop = value

    @property
    def media(self) -> MediaFile:
        """Use media_path instead to set the media to play."""
        return self._media

    @export(None,  "str",   "file_path/med")
    def media_path(self) -> str:
        """Filepath of the attached media file. Read-write."""
        return self._mediapath
    @media_path.setter
    def media_path(self, value):
        self._mediapath = value
        actual_path     = engine.loader._get_true_path(value)
        extensions      = engine.loader.extensions
        extension       = value.split(".")[-1]

        if extension in extensions["vid"]:
            self.media.assign(actual_path, VIDEO)
        elif extension in extensions["sfx"]:
            self.media.assign(actual_path, SOUND)
            if self.citem:
                self.citem.visible = False
        else:
            raise PlayerError("Unknown file extension")
    
    ## Playback functions
    def play(self, keep_play_counter=False):
        """
        Play the attached Media file using the Node's properties.

        Args:
            keep_play_counter:
                Internal argument to decide if the Node should play the attached Media file while keeping the `self._playcounter` value and not resetting it. This is manually used by the `loops` property.
        """
        if self.busy:
            if not self.reset_playback_on_play:
                return
        
        self._media.play()
        if self.media_type == "video":
            self._set_visible(self.visible)
        else:
            if self.citem:
                self._set_visible(False)
    def restart(self):
        """Restart the attached Media file."""
        if not self._playing:
            return
        self._media.restart()
    def stop(self):
        """Stop the attached Media file."""
        self._media.stop()
    def pause(self):
        """Pause the attached Media file."""
        self._media.pause()
    def resume(self):
        """Resume the attached Media file."""
        self._media.resume()
    
    ## Properties
    @property
    def media_type(self):
        return self.media._type
    @property
    def busy(self) -> bool:
        """True if media is playing. Read-only"""
        return self._media.busy
    @property
    def timestamp(self) -> float:
        """Returns the current media timestamp in seconds (float)."""
        return self._media.timestamp
    @property
    def duration(self) -> float:
        """Returns the current media duration in seconds (float)."""
        return self._media.duration
    
    ## Update
    def update(self):
        super().update()
        
        ## Handle playback
        if self.busy:
            if self.media_type == VIDEO:
                self._media._update()
                self.draw()
        else:
            if self._playing:
                self._playcounter += 1
                if self._playcounter < self.loops or self.loops < 0:
                    self.restart()
            if self.citem:
                self.citem.visible = False
    def draw(self):
        if self.media_type == VIDEO and self.media:
            if self.media.frame and self.visible:
                self.citem.image = self.media.frame
                self._set_anchors()
                super().draw()
    
    ## Transform tweaks
    def _set_size(self,w,h):
        self._media.resize(w,h)
    def _set_visible(self, val):
        if not self.busy or self.media_type == SOUND:
            val = False
        super()._set_visible(val)
    
    ## Free
    def _free(self):
        self.stop()
        self._media.free()
        super()._free()