import pygame
from tiles.foundation import Foundation

class CircleParticle(Foundation):
    def __init__(self, groups, pos, max_radius, color, speed):
        super().__init__(groups, type="circle", offgrid_tile = True)
        self.pos = list(pos)
        self.max_radius = max_radius
        self.radius = 0
        self.color = color
        self.speed = speed
        
    def update(self, dt):
        self.radius += self.speed * dt
        
        self.radius = min(self.radius, self.max_radius)
        if self.radius == self.max_radius: self.kill()
    
    def render(self, surf, offset: pygame.Vector2):
        pos = (self.pos[0] - offset.x, self.pos[1] - offset.y)
        pygame.draw.circle(surf, self.color, pos, self.radius, int(20 * (1 - self.radius / self.max_radius) + 1))