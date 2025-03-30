import pygame
from tiles.foundation import Foundation
from math import sin

class Board(Foundation):
    def __init__(self, groups, type: str, pos: tuple[int], size: tuple[int]) -> None:
        super().__init__(groups, type, offgrid_tile=True)
        self.pos = pos
        self.surface_size = size
        self.surface = pygame.Surface(size)
        self.surface.set_alpha(220)
        self.surface.fill('black')
        self.surface_size = pygame.Vector2()
        self.show_surface = False
        self.font = pygame.font.Font('px-4x8/px-4x8.ttf', 12)
        self.text = ''
    
    def show(self, text):
        self.text = str(text)
        self.show_surface = True
        
    def update(self, dt):
        text = self.font.render(self.text, False, 'white')
        text_rect = text.get_rect(center = (self.surface.get_width() / 2, self.surface.get_height() / 2))
        self.surface.blit(text, text_rect)

        delta = 200 * dt
        if self.show_surface:
            self.surface_size.x = min(self.surface_size.x + delta, self.surface.width)
            self.surface_size.y = min(self.surface_size.y + delta, self.surface.height)
        else:
            self.surface_size.x = max(self.surface_size.x - delta, 0)
            self.surface_size.y = max(self.surface_size.y - delta, 0)
        
        self.show_surface = False
    
    def render(self, surf:pygame.Surface, offset: pygame.Vector2):
        y_offset = sin(pygame.time.get_ticks() * 0.005)
        render_image = pygame.transform.scale(self.surface, self.surface_size)
        # render_rect = render_image.get_rect(midbottom = (self.pos[0] - offset.x, self.pos[1] - offset.y - y_offset))
        render_rect = render_image.get_rect(midbottom = (self.pos[0] - offset.x, self.pos[1] - offset.y - y_offset))
        surf.blit(render_image, render_rect)
        self.surface.fill('black')

    

