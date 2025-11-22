# Import libraries
import pyglet as pg
from pygame import Sound, Channel

# Import inherited
from classes.nodes.node  import *

# Classes
class AudioError(Exception):
    pass

class AudioPlayer(Node):
    """
    ## An Audio Player.

    This is a Node that can play audio globally.
    For playing Video, see VideoPlayer.
    """
    def __init__(self, properties={}, parent=None, children=None):
        self._media  : str         = ""
        self._volume : float | int = 0
        self._sound  : Sound       = None
        self.channel : Channel     = None
        self._loops  : int         = 0

        super().__init__(properties, parent, children)
        self._sound   = engine.loader.load(self._media)
        self.sound_id = engine.sid
        engine.sid   += 1
        self.channel  = Channel(self.sound_id)
        if self.get("auto_start"):
            self.play()
    
    @export(0,    "int",   "int")
    def loops(self) -> int: return self._loops
    @loops.setter
    def loops(self, value): self._loops = value

    @property
    def sound(self) -> Sound:
        """Sound object. Read-only."""
        return self._sound
    @sound.setter
    def sound(self,_): raise AudioError("Please replace the audio using `self.media` instead")
    
    @export(None, "str",   "file_path/sfx")
    def media(self) -> str:
        """Filepath of sound. Read-write."""
        return self._media
    @media.setter
    def media(self, value):
        self._media = value
        self._sound = engine.loader.load(value)

    def play(self):
        """
        Play the Sound using the Node's properties.
        """
        self.channel.play(self._sound, self.loops)
    
    def stop(self):
        """
        Stop the Sound.
        """
        self.channel.stop()
    
    def pause(self):
        """
        Pause the Sound.
        """
        self.channel.pause()
    
    def resume(self):
        """
        Resume the Sound.
        """
        self.channel.unpause()
    
    @property
    def busy(self) -> bool:
        """
        True if sound is playing. Read-only
        """
        return self.channel.get_busy()

    @export(1.0, "float", "float")
    def volume(self) -> int:                      return self._volume
    @volume.setter
    def volume(self, value : int | float | None):
        self._volume = value
        self.channel.set_volume(value)