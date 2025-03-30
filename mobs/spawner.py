import pygame
from mobs.enemy1.enemy1 import Enemy
from tiles.groups_picker import *
from tiles.tilemap import TileMap
from particles.circle import CircleParticle
from mobs.boss.basic_boss import Snake

class MobSpawner(TileMap):
    def spawn_enemy(self, map: TileMap, assets: pygame.Surface, pos: tuple[int]) -> Enemy:
        x, y = (pos[0] // self.tile_size) * self.tile_size, (pos[1] // self.tile_size) * self.tile_size
        if len(map.grid_tiles_around(pos, 0)): return

        CircleParticle(groups_picker.get_groups(GroupType.ProceduralParticles), pos, 40, '#964545', 100)

        groups = groups_picker.get_groups(GroupType.Visible, GroupType.Enemy, GroupType.Collidable, GroupType.HitableEntities)
        return Enemy(groups, 'enemy', assets, offgrid_tile=True, topleft=(x, y))

    def spawn_boss(self, assets: pygame.Surface, pos: tuple[int]):
        groups = groups_picker.get_groups(GroupType.Visible, GroupType.Enemy, GroupType.ContactDamage, GroupType.HitableEntities)
        return Snake(groups, 'boss', assets, offgrid_tile=True, center = pos)


    def update(self, dt, player_center):
        for enemy in self.offgrid_tiles: enemy.update(dt, player_center)