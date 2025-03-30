# import pygame

# class ShootParticle:
#     def __init__(self, pos: tuple, velocity: int, direction: pygame.Vector2) -> None:
#         self.x, self.y = pos
#         self.velocity = self.max_velocity = velocity
#         self.direction = direction
    
#     def update(self, dt):
#         self.x += self.direction.x * self.velocity * dt
#         self.y += self.direction.y * self.velocity * dt
#         self.velocity = max(0, self.velocity - dt * 1000)
#         return True if self.velocity else False
    
#     def render(self, display: pygame.Surface, render_offset: pygame.Vector2):
#         points = []
#         render_direction = self.direction
#         multiplier = self.velocity / self.max_velocity

#         for size in (60, 3, 3, 3):
#             posx = self.x - render_offset.x + render_direction.x * size * multiplier
#             posy = self.y - render_offset.y + render_direction.y * size * multiplier
#             points.append((posx, posy))
#             render_direction = render_direction.rotate(90)

#         pygame.draw.polygon(display, 'black', points)

    