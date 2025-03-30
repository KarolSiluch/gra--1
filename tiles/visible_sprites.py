import pygame
from tiles.tilemap import TileMap
from support.settings import *


class YSortCamera(TileMap):
    def __init__(self, tile_size=48) -> None:
        super().__init__(tile_size)


    def print(self):
        tiles = sorted(self.tiles(), key=lambda tile: tile.sprite.rect.centery + tile.sprite.sort_y_offset)
        for tile in tiles: print(f'type: {tile.type}, (x, y): {tile.sprite.rect.center}')


    def render(self, display: pygame.Surface, camera_offset: pygame.Vector2):
        # for tile in sorted(self.all_tiles_around(screen_center, 16), key=lambda tile: (tile.z, tile.sprite.rect.bottom + tile.sprite.sort_y_offset + tile.sprite.render_offset.y)):
        for tile in sorted(self.tiles(), key=lambda tile: (tile.z, tile.sprite.rect.bottom + tile.sprite.sort_y_offset + tile.sprite.render_offset.y)):
            if not tile.sprite.show: continue
            image, rect = tile.get_sprite()
            display.blit(image, rect.topleft - camera_offset + tile.sprite.render_offset, special_flags=tile.special_flags)
