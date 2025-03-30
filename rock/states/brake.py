import pygame
from rock.states.basic_state import BasicState
from cooldown.cooldown import Cooldown

class Brake(BasicState):
    def __init__(self, context, cooldown=0) -> None:
        super().__init__(context, cooldown)
        self.wave_cd = Cooldown(10000)
    
    def _enter(self):
        self.wave_cd.reset()
    
    def update(self, dt, *args):
        self.wave_cd.timer()
        time_ms = self.wave_cd.time_long - (pygame.time.get_ticks() - self.wave_cd.last_used_time)
        self.context.board.show(time_ms // 1000 + 1)
    
    def next_state(self):
        if not self.wave_cd(): return None
        if self.context.current_wave == self.context.waves: return 'final_wave'
        return 'wave'
