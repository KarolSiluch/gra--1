import pygame
from tiles.foundation import Foundation

class Tile(Foundation):
    class Sprite:
        def __init__(self, image: pygame.Surface, sort_y_offset: int = 0, **pos: tuple[int]) -> None:
            self.show = True
            self.flip = False
            self.raw_image = image
            self.final_image = image
            self.rect: pygame.FRect = image.get_frect(**pos)
            self.rect_center = self.rect.center
            self.angle = 0
            self.sort_y_offset = sort_y_offset
            self.render_offset = pygame.Vector2()
        
        def transform(self, angle=0, flip=(False, False), scale=1):
            rotate_image = pygame.transform.flip(self.raw_image, *flip)
            rotate_image = pygame.transform.rotate(rotate_image, angle)
            rotate_image = pygame.transform.scale(rotate_image, (rotate_image.width * scale, rotate_image.height * scale))
            self.rect = rotate_image.get_rect(center = self.rect.center)
            self.final_image = rotate_image
            self.angle = angle
        
        def render_image(self): return self.final_image
        def render_rect(self): return self.rect
        
        
    def __init__(self, groups, type: str, image: pygame.Surface, sort_y_offset: int = 0, offgrid_tile: bool = False, z=5, special_flags=0, **pos: tuple[int]) -> None:
        self.sprite = self.Sprite(image, sort_y_offset, **pos)
        self.hitbox: pygame.FRect = image.get_frect(**pos).inflate(0, -0.6 * image.get_height())
        self.z=z
        self.special_flags = special_flags
        super().__init__(groups, type, offgrid_tile)
    
    def get_sprite(self):
        return (self.sprite.render_image(), self.sprite.render_rect())

    def update(self, dt): ...
        
    
class Entity(Tile):
    def __init__(self, groups, type: str, image: pygame.Surface, sort_y_offset: int = 0, offgrid_tile: bool = False, **pos: tuple[int]) -> None:
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, **pos)
        self.direction = pygame.Vector2()
        self.velocity = 150
        self.acceleration = pygame.Vector2()
    
    
    
