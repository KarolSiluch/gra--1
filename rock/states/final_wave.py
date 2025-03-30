import pygame
from rock.states.basic_state import BasicState
from particles.circle import CircleParticle
from particles.item_spawner import ItemSpawnerParticle
from tiles.groups_picker import *
from mobs.spawner import MobSpawner
from random import randint, choice
from items.potion import Potion
from items.weapon_upgrade import get_modifire

class FinalWave(BasicState):
    def __init__(self, context, game, cooldown=0) -> None:
        super().__init__(context, cooldown)
        self.game = game
        self.enemies = []
        
    
    def spawn(self, dt):
        for spawn_distance in self.spawn_distances:
            if self.particle.radius < spawn_distance: continue

            spawner: MobSpawner = self.game.current_map.sprite_groups[GroupType.Enemy]
            assets = self.game.current_map.game.assets['enemy']
            spawn_offset = pygame.Vector2(0, self.particle.radius).rotate(randint(0, 360))
            pos = (self.context.hitbox.centerx + spawn_offset.x, self.context.hitbox.centery + spawn_offset.y)

            if enemy := spawner.spawn_enemy(self.game.current_map.sprite_groups[GroupType.Collidable], assets, pos): self.enemies.append(enemy)
            self.spawn_distances.remove(spawn_distance)
    
    def _enter(self):
        self.enemies.clear()
        self.spawn_distances = [randint(50, 200) for _ in range(randint(self.context.current_wave * 5, (self.context.current_wave + 1) * 5))]
        self.particle = CircleParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.context.hitbox.center, 200, 'black', 200)
        
    def _exsit(self):
        self.context.waves = randint(2, 5)
        self.context.current_wave = 1
        self.context.spawn_resorce(len(self.enemies))
        CircleParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.context.hitbox.center, 200, '#89daf5', 200)
        

        direction = pygame.Vector2(0, 1).rotate(randint(-70, 70))
        item = Potion('potion', self.game.assets['potion'][0], randint(20, 30))
        ItemSpawnerParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.context.hitbox.midtop, direction, item, '#cbdbfc')

        direction = pygame.Vector2(0, 1).rotate(randint(-70, 70))

        index = randint(1, 2)
        item = get_modifire(self.game.assets['upgrades'][index], index)
        ItemSpawnerParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.context.hitbox.midtop, direction, item, '#45150f')
    
    def update(self, dt, *args):
        self.spawn(dt)
        
    def finished_wave(self):
        if self.particle.radius < self.particle.max_radius: return False
        total_hp = 0
        for enemy in self.enemies: total_hp += enemy.hp
        return not total_hp

    def next_state(self):
        if not self.finished_wave(): return None
        return'compleated'