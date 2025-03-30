from pygame import Surface
from tiles.outlined_tile import OutlinedTile
from particles.board import Board
from tiles.groups_picker import *

class PickableItem(OutlinedTile):
    def __init__(self, groups, item, sort_y_offset: int = 0, offgrid_tile: bool = False, z=5, **pos: tuple[int]) -> None:
        super().__init__(groups, item.type, item.image, sort_y_offset, offgrid_tile, z, **pos)
        self.item = item
        self.board = Board(groups_picker.get_groups(GroupType.ProceduralParticles), 'board', (self.hitbox.centerx, self.hitbox.centery - 8), (80, 16))

    def interact(self, player):
        self.show_outline()
        self.board.show(self.item.get_information())
        if player.using_e:
            self.item.interact(player)
            self.kill()