import pygame
from tiles.tile import Tile
from tiles.foundation import Foundation
from tiles.groups_picker import *

class Leaves(Tile):
    def sway(self, wind: pygame.Vector2):
        self.sprite.render_offset.x = wind.x
        self.sprite.render_offset.y = abs(wind.y) * 0.5

class Tree(Foundation):
    def __init__(self, type: str, pos: tuple, assets, offgrid_tile: bool = False) -> None:
        self.hitbox = assets[0].get_rect(midbottom = pos)
        super().__init__(groups_picker.get_groups(GroupType.Trees), type, offgrid_tile)
        self.wind = pygame.Vector2(1, 0)
        self.trunk = Tile(groups_picker.get_groups(GroupType.Visible), 'trunk', assets[0], z=6, midbottom=pos)
        self.create_the_tree(pos, assets[1:])
        
    def create_the_tree(self, pos, assets):
        self.leaves = []
        total_offset = 0
        z = 0
        for offset, image in zip([7, 18, 20], assets):
            x, y = pos
            z += 0.1
            total_offset += offset
            leave = Leaves(groups_picker.get_groups(GroupType.Visible), 'leaves', image, z=6 + z, midbottom=(x, y - total_offset))
            self.leaves.append(leave)
    
    def update(self, dt):
        for index, leave in enumerate(self.leaves):
            leave.sway(self.wind.rotate(index * 45))
        self.wind.rotate_ip(dt * 200)
    
    def kill(self):
        self.trunk.kill()
        for leave in self.leaves: leave.kill()
        super().kill()

        
    