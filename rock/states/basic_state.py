import pygame
from cooldown.cooldown import Cooldown

class BasicState:
    def __init__(self, context, cooldown=0) -> None:
        self.context = context
        self.cooldown = Cooldown(cooldown)
    
    def interact(self, player): ...
        
    def _enter(self): ...

    def _exsit(self):
        self.cooldown.reset()

    def update(self, dt, *args): ...

    def next_state(self): return None