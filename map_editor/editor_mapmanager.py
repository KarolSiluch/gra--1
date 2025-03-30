import pygame
import json

from map_editor.editor_tile import EditorTile
from tiles.visible_sprites import YSortCamera
from mouse.mouse import coursor
from support.support import load_image
from tiles.tile import Tile


class EditorMapManager:
    def __init__(self, game, tile_size: int) -> None:
        self.game = game
        self.tile_size = tile_size
        self.camera_offset = pygame.Vector2()
        self.sprite_group = YSortCamera(tile_size)

        try: self.load('map2.json')
        except FileNotFoundError: pass
    
    def save(self, path):
        f = open(path, 'w')
        tilemap = []
        for tile in self.sprite_group.tiles():
            if tile.type == 'background': continue
            tilemap.append({'type': tile.type, 'variant': tile.variant, 'offgrid_tile': tile.offgrid_tile, 'z': tile.z, 'pos': tile.created_position})

        json.dump({'tilemap': tilemap, 'tile_size': self.tile_size}, f)
        f.close()
    
    def load(self, path):
        background = load_image('assets/map2/background.png')
        Tile([self.sprite_group], 'background', background, offgrid_tile=True, z=0, topleft = (0, 0))
        
        f = open(path, 'r')
        map_date = json.load(f)
        f.close()
        for tile_data in map_date['tilemap']:
            type = tile_data['type']
            variant = tile_data['variant']
            image = self.game.assets[type][variant]
            offgrid_tile = tile_data['offgrid_tile']
            layer = tile_data['z'] 
            pos = tile_data['pos'] 
            EditorTile([self.sprite_group], type, variant, image, offgrid_tile=offgrid_tile, z=layer, **pos)
    
    def update(self, dt):
        coursor.update(self.camera_offset)
    
    def get_camera_offset(self, display):
        self.camera_offset = self.game.camera_offset

    def render(self, display: pygame.Surface):
        self.get_camera_offset(display)
        self.sprite_group.render(display, self.camera_offset)