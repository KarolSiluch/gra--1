from enum import Enum
from tiles.tilemap import TileMap


class GroupType(Enum):
    Visible = 1
    Collidable = 2
    Grass = 3
    Bullets = 4
    ProceduralParticles = 5
    Trees = 6
    Activitable = 7
    Enemy = 8
    HitableEntities = 9
    ContactDamage = 10


class GroupsPicker:
    def init(self, groups) -> None:
        self.groups = groups

    def get_groups(self, *group_types) -> list[TileMap]:
        sprite_groups = []
        for type in group_types:
            sprite_groups.append(self.groups[type])
        return sprite_groups

    def get_group(self, type: GroupType) -> TileMap:
        return self.groups[type]


groups_picker = GroupsPicker()
