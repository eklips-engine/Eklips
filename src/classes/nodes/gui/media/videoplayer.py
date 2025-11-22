# Import libraries
import pyglet as pg
from pygame import Sound, Channel

# Import inherited
from classes.nodes.gui.canvasitem import *

# Classes
class VideoError(Exception):
    pass

class VideoPlayer(CanvasItem):
    """
    ## A Video Player.

    This is a Node that can play video and display it on the screen.
    For playing Audio, see AudioPlayer.
    """
    _ignore_size_if_drawing               = True
    
    def __init__(self, properties={}, parent=None, children=None):
        self._media       : str                    = ""
        self._volume      : float | int            = 0
        self._playcounter : int                    = 0
        self._playing     : bool                   = False
        self._video       : engine.pvd.VideoPyglet = None
        self._media       : str                    = ""
        self._ogsize      : list[int]              = [100,100]
        self._tmpfilepath : str                    = None
        self._loops       : int                    = 0

        super().__init__(properties, parent, children)
        self._make_new_sprite()
        if self.get("auto_start"):
            self.play()
    
    def update(self):
        super().update()
        self.w, self.h = self._ogsize
        if self._video.active:
            self._video._update()
            self.draw(self._video.frame_surf)
        else:
            if self._playing:
                self._playcounter += 1
                self.playing       = False
                if self._playcounter < self.get("loops",0) or self.get("loops", 0) == -1:
                    self.restart()
    
    def draw(self, image):
        if image:
            self._draw(image)
    
    def _draw(self, image):
        return engine.display.blit(
            surface        = image,
            transform      = self,
            window_id      = self.window_id,
            sprite         = self.sprite,
            group          = self._canvas_layer,
            ignore_scaling = True
        )
    
    def _set_size(self,w,h):
        size = [round(w),round(h)]
        self._video.resize(size)
    
    @export(0,    "int",   "int")
    def loops(self) -> int: return self._loops
    @loops.setter
    def loops(self, value): self._loops = value
    
    @property
    def video(self) -> engine.pvd.VideoPyglet:
        """Video object. Read-only."""
        return self._video
    @video.setter
    def video(self,_): raise VideoError("Please replace the video using `self.media` instead.")
    
    @export(None, "str",   "file_path/vid")
    def media(self) -> str:
        """Filepath of video. Read-write."""
        return self._media
    @media.setter
    def media(self, value):
        self._media  = value
        self._video  = engine.pvd.VideoPyglet(engine.loader._get_true_path(self._media))
        self._ogsize = self._video.current_size
        self._video.stop()
    
    def play(self):
        """
        Play the Video using the Node's properties.
        """
        self._playing     = True
        self._playcounter = 0
        self._video.play()
    
    def restart(self):
        """
        Restart the Video.
        """
        self._video.restart()
    
    def stop(self):
        """
        Stop the Video.
        """
        self._playing     = False
        self._video.stop()
    
    def pause(self):
        """
        Pause the Video.
        """
        self._video.pause()
    
    def resume(self):
        """
        Resume the Video.
        """
        self._video.resume()
    
    @property
    def busy(self):
        """
        True if Video is playing. Read-only
        """
        return self._video.active

    @export(1.0, "float", "float")
    def volume(self) -> int:                      return self._volume
    @volume.setter
    def volume(self, value : int | float | None):
        self._volume = value
        self._video.set_volume(value)