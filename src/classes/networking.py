## Import components
import classes.singleton as engine
import socket       as sock
from classes        import resources
from classes.locals import *

## Classes
class Packet:
    def __init__(self, data=""):
        self.header = PACKET_BASIC
        self._size  = -1
        self._data  = ""

        self.data   = data
    
    def __repr__(self):
        return self.networking_form
    @property
    def networking_form(self):
        form = f"{self.header}{' '*(len(self.header)-4)}{self.size}{self.data}"
        return f"{len(form)}{form}".encode()
    @property
    def size(self): return len(self._data)
    @property
    def data(self): return self._data
    @data.setter
    def data(self, value):
        self._data = value
        self.size  = len(value)