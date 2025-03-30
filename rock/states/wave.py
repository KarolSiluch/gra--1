import pygame
from rock.states.basic_state import BasicState
from particles.circle import CircleParticle
from particles.item_spawner import ItemSpawnerParticle
from tiles.groups_picker import *
from mobs.spawner import MobSpawner
from random import randint, choice
from items.potion import Potion

class Wave(BasicState):
    def __init__(self, context, game, cooldown=0) -> None:
        super().__init__(context, cooldown)
        self.game = game
        self.enemies = []
        
    def spawn(self, dt):
        for spawn_distance in self.spawn_distances:
            if self.particle.radius < spawn_distance: continue

            spawner: MobSpawner = groups_picker.get_group(GroupType.Enemy)
            assets = self.game.current_map.game.assets['enemy']
            spawn_offset = pygame.Vector2(0, self.particle.radius).rotate(randint(0, 360))
            pos = (self.context.hitbox.centerx + spawn_offset.x, self.context.hitbox.centery + spawn_offset.y)

            if enemy := spawner.spawn_enemy(groups_picker.get_group(GroupType.Collidable), assets, pos): self.enemies.append(enemy)
            self.spawn_distances.remove(spawn_distance)
    
    def _enter(self):
        self.enemies.clear()
        self.spawn_distances = [randint(50, 200) for _ in range(randint(self.context.current_wave * 5, (self.context.current_wave + 1) * 5))]
        self.particle = CircleParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.context.hitbox.center, 200, '#964545', 200)
        
    def _exsit(self):
        self.context.spawn_resorce(len(self.enemies))
        self.context.current_wave += 1
            
        direction = pygame.Vector2(0, 1).rotate(randint(-70, 70))
        item = Potion('potion', self.game.assets['potion'][0], randint(10, 20))
        ItemSpawnerParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.context.hitbox.midtop, direction, item, '#cbdbfc')
    
    def update(self, dt, *args):
        self.spawn(dt)
        
    def finished_wave(self):
        if self.particle.radius < self.particle.max_radius: return False
        total_hp = 0
        for enemy in self.enemies: total_hp += enemy.hp
        return not total_hp

    def next_state(self):
        if not self.finished_wave(): return None
        return 'brake'
        
        
        