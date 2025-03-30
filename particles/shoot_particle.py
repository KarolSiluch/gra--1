import pygame
from tiles.foundation import Foundation

class ShootParticle(Foundation):
    def __init__(self, groups, pos, direction: pygame.Vector2, speed, color):
        super().__init__(groups, type="shoot_particle", offgrid_tile = True)
        self.pos = list(pos)
        self.direction = direction
        self.speed = speed
        self.color = color
        
    def update(self, dt):
        self.pos[0] += self.direction.x * self.speed * dt
        self.pos[1] += self.direction.y * self.speed * dt
        
        self.speed = max(0, self.speed - dt * 1000)
        if not self.speed: self.kill()
    
    def render(self, surf, offset: pygame.Vector2):
        render_points = []
        render_direction = self.direction

        for size in [3, 0.5, 3, 0.5]:
            x = self.pos[0] + render_direction.x * self.speed * size // 60 - offset.x
            y = self.pos[1] + render_direction.y * self.speed * size // 60 - offset.y
            render_points.append((x, y))
            render_direction.rotate_ip(90)
        
        pygame.draw.polygon(surf, self.color, render_points)
        
