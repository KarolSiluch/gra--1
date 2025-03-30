import pygame
import json
from tiles.tilemap import TileMap
from tiles.tile import Tile
from tiles.visible_sprites import YSortCamera
from grass import GrassManages
from mouse.mouse import coursor
from particles.procedural_particles_group import ProceduralParticleGroup
from trees.tree import Tree
from tiles.groups_picker import *
from rock.rock import Rock
from mobs.spawner import MobSpawner

class MapManager:
    def __init__(self, game, tile_size: int, map: str, stage: int) -> None:
        self.game = game
        self.tile_size = tile_size
        self.camera_offset = pygame.Vector2()
        self.map = map
        self.sprite_groups = {
            GroupType.Visible: YSortCamera(tile_size),
            GroupType.Collidable: TileMap(tile_size),
            GroupType.Grass: GrassManages(tile_size),
            GroupType.Bullets: TileMap(tile_size),
            GroupType.ProceduralParticles: ProceduralParticleGroup(tile_size),
            GroupType.Trees: TileMap(tile_size),
            GroupType.Activitable: TileMap(tile_size),
            GroupType.Enemy: MobSpawner(tile_size),
            GroupType.HitableEntities: TileMap(tile_size),
            GroupType.ContactDamage: TileMap(tile_size)
        }
        groups_picker.init(self.sprite_groups)

        self.player_start_position = (0, 0)

        try: self.load(f'{map}.json', stage)
        except FileExistsError: pass

        self.add_shadows()

    def enter(self):
        groups_picker.init(self.sprite_groups)

    def add_shadows(self):
        map: TileMap = self.sprite_groups[GroupType.Collidable]
        for pos, tiles in map.tile_map.items():
            if 'rock' in set([tile.type for tile in tiles]): continue
            if 'border' in set([tile.type for tile in tiles]): continue
            x, y = pos
            shadow_tiles = self.game.assets['shadows']

            if (x, y + 1) not in map.tile_map.keys():
                surface = pygame.Surface((self.tile_size, self.tile_size))
                surface.fill('white')
                surface.set_colorkey('white')
                surface.blit(shadow_tiles[3], (0, 0))

                offsets = ((1, 0), (-1, 0), (1, 1), (-1, 1))
                image_inbers = (9, 6, 1, 0)
                for offset, image_number in zip(offsets, image_inbers):
                    if (x + offset[0], y + offset[1]) in map.tile_map.keys():
                        surface.blit(shadow_tiles[image_number], (0, 0))

                pos = (x * self.tile_size, (y + 1) * self.tile_size)
                Tile(groups_picker.get_groups(GroupType.Visible), 'shadow', surface, z=1, special_flags=pygame.BLEND_RGB_MIN, topleft=pos)

            if (x + 1, y) not in map.tile_map.keys():
                surface = pygame.Surface((self.tile_size, self.tile_size))
                surface.fill('white')
                surface.set_colorkey('white')
                surface.blit(shadow_tiles[2], (0, 0))

                offsets = ((0, 1), (0, -1), (1, -1))
                image_inbers = (5, 8, 0)
                for offset, image_number in zip(offsets, image_inbers):
                    if (x + offset[0], y + offset[1]) in map.tile_map.keys():
                        surface.blit(shadow_tiles[image_number], (0, 0))

                pos = ((x + 1) * self.tile_size, y * self.tile_size)
                Tile(groups_picker.get_groups(GroupType.Visible), 'shadow', surface, z=1, special_flags=pygame.BLEND_RGB_MIN, topleft=pos)

            if (x - 1, y) not in map.tile_map.keys():
                surface = pygame.Surface((self.tile_size, self.tile_size))
                surface.fill('white')
                surface.set_colorkey('white')
                surface.blit(shadow_tiles[4], (0, 0))

                offsets = ((0, 1), (0, -1), (-1, -1))
                image_inbers = (10, 7, 1)
                for offset, image_number in zip(offsets, image_inbers):
                    if (x + offset[0], y + offset[1]) in map.tile_map.keys():
                        surface.blit(shadow_tiles[image_number], (0, 0))

                pos = ((x - 1) * self.tile_size, y * self.tile_size)
                Tile(groups_picker.get_groups(GroupType.Visible), 'shadow', surface, z=1, special_flags=pygame.BLEND_RGB_MIN, topleft=pos)



    def load(self, path, stage):
        Tile(groups_picker.get_groups(GroupType.Visible), 'background',self.game.assets['background'][self.map], offgrid_tile=True, z=0, topleft=(0, 0))
        f = open(path, 'r')
        map_date = json.load(f)
        f.close()
        for tile_data in map_date['tilemap']:
            self.create_tile(tile_data, stage)
        print(self.sprite_groups[GroupType.Grass].blades_number())

    def create_tile(self, tile_data, stage):
        type = tile_data['type']
        variant = tile_data['variant']
        offgrid_tile = tile_data['offgrid_tile']
        layer = tile_data['z']
        pos: dict = tile_data['pos']


        if type in {'grass'}:
            grass_manager: GrassManages = self.sprite_groups[GroupType.Grass]
            groups = groups_picker.get_groups(GroupType.Visible)
            assets = self.game.assets[type]
            x, y = list(pos.values())[0]
            grass_manager.spawn_grass(groups, assets, (x // self.tile_size, y // self.tile_size), 4)

        elif type in {'pine_tree'}:
            pos = list(pos.values())[0]
            assets = self.game.assets[type]
            Tree(type, pos, assets, offgrid_tile=False)

        elif type in {'rock'}:
            groups = groups_picker.get_groups(GroupType.Visible, GroupType.Collidable, GroupType.Activitable)
            image = self.game.assets[type][variant]
            Rock(groups, type, image, self.game, stage, offgrid_tile=offgrid_tile, z=layer, **pos)

        elif type in {'wall', 'lab_wall'}:
            groups = groups_picker.get_groups(GroupType.Visible, GroupType.Collidable)
            image = self.game.assets[type][variant]
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

        elif type in {'border'}:
            groups = groups_picker.get_groups(GroupType.Collidable)
            image = pygame.Surface((self.tile_size, self.tile_size))
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

        elif type == 'player': self.player_start_position = list(pos.values())[0]

        else:
            groups = groups_picker.get_groups(GroupType.Visible)
            image = self.game.assets[type][variant]
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

    def update(self, dt):
        coursor.update(self.camera_offset)
        self.sprite_groups[GroupType.Grass].update(dt, self.game.player.hitbox.center)
        self.sprite_groups[GroupType.Trees].update(dt, self.game.player.hitbox.center)
        self.sprite_groups[GroupType.ProceduralParticles].update(dt, self.game.player.hitbox.center)
        self.sprite_groups[GroupType.Bullets].update(dt, self.game.player.hitbox.center, self)
        self.sprite_groups[GroupType.Activitable].update(dt, self.game.player.hitbox.center)
        self.sprite_groups[GroupType.Enemy].update(dt, self.game.player.hitbox.center)
        for tile in self.sprite_groups[GroupType.ContactDamage].offgrid_tiles:
            tile.contact_damage(self.game.player)

    def get_camera_offset(self, display: pygame.Surface):
        mouse_vector = coursor.mouse_vector(self.game.player.hitbox.center)
        vector_size = min(mouse_vector.magnitude() / 7, 60)
        if mouse_vector.magnitude(): mouse_vector.scale_to_length(vector_size)

        mouse_offset_x = self.game.player.hitbox.centerx + mouse_vector.x
        mouse_offset_y = self.game.player.hitbox.centery + mouse_vector.y

        self.camera_offset.x += (mouse_offset_x - display.get_width() // 2 - self.camera_offset.x) / 10
        self.camera_offset.y += (mouse_offset_y - display.get_height() // 2 - self.camera_offset.y) / 10

    def render(self, display: pygame.Surface):
        self.get_camera_offset(display)
        self.sprite_groups[GroupType.Visible].render(display, self.camera_offset)
        self.sprite_groups[GroupType.ProceduralParticles].render(display, self.camera_offset)

    # def import_assets(self, map):
    #     self.assets = {

    #     }