import pygame
from cooldown.cooldown import Cooldown

class BasicState:
    def __init__(self, context, possible_next_states: set[str], cooldown=0) -> None:
        self.context = context
        self.cooldown = Cooldown(cooldown)
        self.possible_next_states = possible_next_states
        
    def _enter(self): ...

    def contact_damage(self, damage, direction): ...

    def _exsit(self):
        self.cooldown.reset()

    def animate(self, dt):
        direction = self.context.sprite.flip * 2 - 1
        direction = direction if self.context.direction.x < 0 else - direction
        direction = 1 if self.context.direction.x == 0 else direction
        self.context.current_animation.update(dt, direction)

    def update(self, dt, *args):
        self.animate(dt)

    def next_state(self, events): ...