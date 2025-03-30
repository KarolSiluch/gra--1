from states.player_run import PlayerRunState
from tiles.tile import Tile
import pygame

class ContactDamage(PlayerRunState):    
    def _enter(self):
        self.context.change_animation('idle')
        self.context.velocity = 250
        self.context.can_be_shot = False
    
    def pass_information(self, contact_diraction: pygame.Vector2):
        self.contact_direction = contact_diraction

    def update(self, dt, tile_map):
        super().update(dt, tile_map)
        self.move(dt, tile_map, self.contact_direction)
        self.context.velocity -= dt * 500

    def _exsit(self):
        self.cooldown.reset()
        self.context.velocity = 150
        self.context.can_be_shot = True
    
    def next_state(self, events):
        if self.context.velocity > 50: return
        if self.context.direction.magnitude(): return 'idle'
        return 'idle'
        