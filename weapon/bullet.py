import pygame
from support.support import vector_angle
from tiles.tile import Tile
from cooldown.cooldown import Cooldown
from particles.shoot_particle import ShootParticle
from tiles.groups_picker import *
from random import randint
from tiles.tilemap import TileMap

COLLIDABLE_TILES = {'wall', 'rock', 'lab_wall'}

class Bullet(Tile):
    def __init__(self, groups, image: pygame.Surface, direction: pygame.Vector2, speed: int, sent_by, sort_y_offset=0, **pos: tuple[int]) -> None:
        super().__init__(groups, 'bullet', pygame.transform.rotate(image, vector_angle(direction)), sort_y_offset = sort_y_offset, offgrid_tile=True, z=6, **pos)
        self.hitbox = image.get_frect(**pos)
        self.direction = direction
        self.speed = speed
        self.life_time = Cooldown(1000)
        self.life_time.can_perform = False
        self.sent_by = sent_by
    
    def hit_something(self, map):
        collidable_tiles: TileMap = map.sprite_groups[GroupType.Collidable]
        for tile in collidable_tiles.get_collisions(self, 0):
            if not tile.type in COLLIDABLE_TILES: continue
            self.kill()
        
        entities: TileMap = map.sprite_groups[GroupType.HitableEntities]
        for entity in entities.get_collisions(self, 0):
            if entity.type == self.sent_by: continue
            if not entity.can_be_shot: continue
            entity.get_hit()
            self.kill()


    def move(self, dt, tile_map):
        self.hitbox.x += self.direction.x * self.speed * dt
        self.hitbox.y += self.direction.y * self.speed * dt
        self.hit_something(tile_map)

        self.sprite.rect.center = self.hitbox.center
         
    def update(self, dt, tilemap):
        self.life_time.timer()
        if self.life_time(): self.kill()
        self.move(dt, tilemap)
    
    def kill(self):
        for _ in range(3): ShootParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.hitbox.center, self.direction.rotate(randint(0, 360)), randint(100, 200), 'black')
        return super().kill()