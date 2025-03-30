import pygame
from tiles.foundation import Foundation
from random import randint
from items.pickable_item import PickableItem
from tiles.groups_picker import *

def get_circle(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey('black')
    return surf

class ItemSpawnerParticle(Foundation):
    def __init__(self, groups, pos, direction: pygame.Vector2, item, color):
        super().__init__(groups, type="item_spawner", offgrid_tile = True)
        self.pos = list(pos)
        self.star_point = list(pos)

        self.direction = direction
        self.distance = 60

        self.y_offset = lambda x: -0.07 * (x - self.distance) * x
        self.z = 0

        self.color = color
        self.speed = 80
        self.radius = 4

        self.item = item
        
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        displacement = pygame.Vector2(self.pos[0] - self.star_point[0], self.pos[1] - self.star_point[1])
        magnitude = min(displacement.magnitude(), self.distance)
        
        self.z = self.y_offset(magnitude)
        
        if magnitude == self.distance:
            PickableItem(groups_picker.get_groups(GroupType.Visible, GroupType.Activitable), self.item, center = self.pos)
            self.kill()
    
    def render(self, surf: pygame.Surface, offset: pygame.Vector2):
        pos = (self.pos[0] - offset.x, self.pos[1] - offset.y - self.z)
        backlight_image = get_circle(self.radius  * 2, (30, 30, 30))
        backlight_rect = backlight_image.get_rect(center = pos)
        surf.blit(backlight_image, backlight_rect, special_flags=pygame.BLEND_RGB_ADD)
        
        image2 = get_circle(self.radius, self.color)
        rect2 = image2.get_rect(center = pos)
        surf.blit(image2, rect2)