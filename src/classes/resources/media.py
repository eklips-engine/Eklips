## Import singleton
import pyglet as pg
from classes.resources.resource import *
from classes.types              import *
from pyglet.media               import Source, Player
from pyvidplayer2.video_pyglet  import VideoPyglet as Video

## Media wrapper
class MediaFile(Resource):
    def __init__(self, properties={}):
        super().__init__(properties)

        self._path    : str | None     = None
        self._type    : str | None     = None
        self._ogsize  : list[int]      = [0,0]
        self._media   : Source | Video = None
        self._playing : bool           = False
        self._player  : Player         = None

    @property
    def frame(self):
        if self._media and self._type == VIDEO:
            return self._media.frame_surf
    @property
    def duration(self):
        if self._media:
            if self._media.duration == None:
                return 0
            return self._media.duration
    @property
    def timestamp(self):
        if self._media:
            if self._type == VIDEO:
                return self._media.active
            else:
                return self._player.time
    @property
    def busy(self):
        if not self._playing:
            return False
        if self._type == VIDEO:
            return self._media.active
        else:
            if not self._media:
                return False
            return (not self._player.playing) and (self.timestamp >= self.duration)
    
    @property
    def volume(self):
        if not self._media:
            return 0
        
        if self._type == VIDEO:
            return self._media.volume
        else:
            if not self._player:
                return 0
            return self._player.volume
    @volume.setter
    def volume(self, value):
        if not self._media:
            return 0
        
        if self._type == VIDEO:
            self._media.set_volume(value)
        else:
            if not self._player:
                return 0
            self._player.volume = value

    ## Transform
    def resize(self, w, h):
        if self._media and self._type == VIDEO:
            self._media.resize((w, h))
    
    ## Playback functions
    def play(self):
        if not self._media:
            return
        self._playing  = True
        if self._type == SOUND:
            if not self._player:
                self._player = Player()
            self._player.next_source()
            self._player.queue(self._media)
            self._player.play()
        else:
            self._media.play()
    def restart(self):
        self._playing  = True
        if self._type == SOUND:
            if self._player:
                self._player.pause()
                self._player.seek(0.0)
                self._player.play()
        else:
            if self._media:
                self._media.restart()
    def stop(self):
        self._playing  = False
        if self._type == SOUND:
            if self._player:
                self._player.pause()
        else:
            if self._media:
                self._media.stop()
    def pause(self):
        if self._type == SOUND:
            if self._player:
                self._player.pause()
        else:
            if self._media:
                self._media.pause()
    def resume(self):
        if self._type == SOUND:
            if self._player:
                self._player.play()
        else:
            if self._media:
                self._media.resume()
    
    def assign(self, media_path, media_type):
        self._type = media_type
        self._path = media_path

        if media_type == "video":
            self._media  = Video(pg.resource.file(media_path))
            self._ogsize = self._media.current_size
        else:
            self._media = pg.resource.media(media_path)