from pygame import Surface
from tiles.tile import Tile

class EditorTile(Tile):
    def __init__(self, groups, type: str, variant: int, image: Surface, sort_y_offset: int = 0, offgrid_tile: bool = False, z=5, **pos: tuple[int]) -> None:
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, z, **pos)
        self.variant = variant
        self.created_position = pos
        