from states.basic_state import BasicState
from tiles.tile import Tile
import pygame

COLLIDABLE_TILES = {'wall', 'rock', 'enemy', 'lab_wall', 'border'}

class PlayerRunState(BasicState):    
    def _enter(self):
        self.context.change_animation('run')

    def move(self, dt, tile_map, direction: pygame.Vector2):
        self.context.hitbox.x += direction.x * self.context.velocity * dt
        collisions: list[Tile] = tile_map.get_collisions(self.context)
        for tile in collisions:
            if not tile.type in COLLIDABLE_TILES: continue
            if direction.x > 0: self.context.hitbox.right = tile.hitbox.left
            elif direction.x < 0: self.context.hitbox.left = tile.hitbox.right
    
        self.context.hitbox.y += direction.y * self.context.velocity * dt
        collisions: list[Tile] = tile_map.get_collisions(self.context)
        for tile in collisions:
            if not tile.type in COLLIDABLE_TILES: continue
            if direction.y > 0: self.context.hitbox.bottom = tile.hitbox.top
            elif direction.y < 0: self.context.hitbox.top = tile.hitbox.bottom
        
        self.context.sprite.rect.center = self.context.hitbox.center

    def update(self, dt, tile_map):
        super().update(dt)
        self.move(dt, tile_map, self.context.direction)
    
    def next_state(self, events):
        if not self.context.direction.magnitude(): return 'idle'
        if events['shift']: return 'dodge'
