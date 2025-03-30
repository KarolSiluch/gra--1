from tiles.tile import Entity
import pygame
from states.state_machine import StateMachine
from animation.animation import Animation

class AnimatedTile(Entity):
    def __init__(self, groups, type: str, animations, first_state, render_y_offset: int = 0, offgrid_tile: bool = False, **pos) -> None:
        self.animations = animations 
        self.current_animation: Animation = self.animations[first_state].copy()   
        super().__init__(groups, type, self.current_animation.img(), render_y_offset, offgrid_tile, **pos)
        
    def animate(self):
        self.sprite.raw_image = self.current_animation.img()
    
    def change_animation(self, state):
        self.current_animation = self.animations[state].copy()