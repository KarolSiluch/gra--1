from states.basic_state import BasicState
from tiles.tile import Tile

class PlayerIdleState(BasicState):
    def _enter(self):
        self.context.change_animation('idle')
    
    def next_state(self, events):
        if self.context.direction.magnitude(): return 'run'
        