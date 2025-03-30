import pygame
from player.player import Player

class HealthBar:
    def __init__(self, player: Player, size: tuple[int], pos: tuple[int]) -> None:
        self.player = player
        self.surface = pygame.Surface(size)
        self.displayed_hp = self.player.hp
        self.pos = pos
    
    def render(self, surf: pygame.Surface):
        if self.player.hp < 0: return
        
        self.surface.fill('#1d1c23')
        if self.displayed_hp > self.player.hp:
            pygame.draw.rect(self.surface, 'white', pygame.Rect(0, 0, (self.displayed_hp / self.player.max_hp) * self.surface.width, self.surface.height))
            pygame.draw.rect(self.surface, '#3f3f74', pygame.Rect(0, 0, (self.player.hp / self.player.max_hp) * self.surface.width, self.surface.height))
        else:
            pygame.draw.rect(self.surface, 'white', pygame.Rect(0, 0, (self.player.hp / self.player.max_hp) * self.surface.width, self.surface.height))
            pygame.draw.rect(self.surface, '#3f3f74', pygame.Rect(0, 0, (self.displayed_hp / self.player.max_hp) * self.surface.width, self.surface.height))
            
        surf.blit(self.surface, self.pos)
    
    def update(self, dt):
        if self.displayed_hp > self.player.hp:
            self.displayed_hp = max(self.player.hp, self.displayed_hp - 10 * dt)
        else:
            self.displayed_hp = min(self.player.hp, self.displayed_hp + 10 * dt)