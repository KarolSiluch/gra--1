import pygame
from rock.states.basic_state import BasicState
from particles.circle import CircleParticle
from particles.item_spawner import ItemSpawnerParticle
from tiles.groups_picker import *
from mobs.spawner import MobSpawner
from random import randint, choice
from items.potion import Potion
from tiles.tilemap import TileMap

class BossFight(BasicState):
    def __init__(self, context, game, cooldown=0) -> None:
        super().__init__(context, cooldown)
        self.game = game
    
    def _enter(self):
        spawner: MobSpawner = self.game.current_map.sprite_groups[GroupType.Enemy]
        assets = self.game.current_map.game.assets['boss']

        print(self.game.current_map.map)

        self.boss = spawner.spawn_boss(assets, (320, 320))
    
    def _exsit(self):
        self.context.spawn_resorce(30)
            
        direction = pygame.Vector2(0, 1).rotate(randint(-70, 70))
        item = Potion('potion', self.game.assets['potion'][0], randint(10, 20))
        ItemSpawnerParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.context.hitbox.midtop, direction, item, '#cbdbfc')

    def next_state(self):
        if self.boss.is_alive(): return None
        return 'compleated'