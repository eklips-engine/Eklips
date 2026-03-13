# Import libraries
from classes.nodes.twod.collisionbox import *

# Classes
class Body(CollisionBox):
    """
    A CollisionBox which abides the laws of 2D physics.

    XXX
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
    
    def __init__(self, properties={}, parent=None):
        self._velocity = [0,0]
        self._noclip   = False
        super().__init__(properties, parent)
    
    def update(self):
        super().update()

        if self.world.get_collisions(self):
            self._velocity[0] = 0
        if self.world.get_collisions(self):
            self._velocity[1] = 0
        self.x += self._velocity[0]
        self.y += self._velocity[1]