# Import libraries
from classes.nodes.twod.collisionbox import *

# Classes
class Body(CollisionBox):
    """
    A CollisionBox which abides the laws of 2D physics.
    """

    @property
    def velocity(self):
        return self._velocity
    @velocity.setter
    def velocity(self, value):
        self._velocity = value
    @export(False, "bool", "bool")
    def noclip(self):
        return self._noclip
    @noclip.setter
    def noclip(self, value):
        self._noclip = value
    
    @property
    def on_ground(self):
        return self._onground
    @property
    def on_wall(self):
        return self._onwall
    
    def __init__(self, properties={}, parent=None):
        self._velocity = [0,0]
        self._noclip   = False
        self._onground = False
        self._onwall   = False
        super().__init__(properties, parent)
    
    def update(self):
        super().update()

        if not self.noclip:
            self.x += self._velocity[0]
            if self.world.get_collisions(self):
                self.x           -= self._velocity[0]
                self._velocity[0] = 0
                self._onwall      = True
            else:
                self._onwall      = False
            
            self.y += self._velocity[1]
            if self.world.get_collisions(self):
                self.y           -= self._velocity[1]
                self._velocity[1] = 0
                self._onground    = True
            else:
                self._onground    = False