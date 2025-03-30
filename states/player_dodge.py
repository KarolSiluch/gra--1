import pygame
from states.player_run import PlayerRunState
from math import copysign

class PlayerDodgeState(PlayerRunState):
    def __init__(self, context, next_possible_states, cooldown=0) -> None:
        super().__init__(context, next_possible_states, cooldown)
        self.angle = 0
        self.y_offset = lambda x: 0.0003 * (x - 360) * x
        
    
    def _enter(self):
        self.angle = 0
        self.context.velocity = 350
        self.context.change_animation('dodge')
        self.set_direction = self.context.direction
        self.context.weapon.can_shoot = False
        self.context.can_be_shot = False
    
    def _exsit(self):
        self.cooldown.reset()
        self.context.sprite.angle = 0
        self.context.velocity = 150
        self.context.weapon.visual_representation.sprite.scale = 1
        self.context.weapon.can_shoot = True
        self.context.can_be_shot = True
    
    def animate(self, dt):
        frame = abs(self.angle) * self.context.current_animation.length() / 360
        self.context.current_animation.update(dt, frame)
    
    def update(self, dt, tile_map):
        self.angle += dt * 1000
        self.context.sprite.angle = -copysign(self.angle, self.set_direction.x)
        self.context.weapon.visual_representation.sprite.scale = max(0, 1 - self.angle / 200)
        self.context.sprite.render_offset.y = self.y_offset(self.angle)
        self.move(dt, tile_map, self.set_direction)
        self.animate(dt)
    
    def next_state(self, events):
        if self.angle < 360: return None
        if self.context.direction.magnitude(): return 'run'
        return 'idle'

