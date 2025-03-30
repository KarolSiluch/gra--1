import pygame
from player.player import Player
from ui.helth_bar import HealthBar
from particles.procedural_particles_group import ProceduralParticleGroup
from ui.modifire_display import ModifireDisplay
from tiles.mapmanager import MapManager
from tiles.groups_picker import *

class UserInterface:
    def __init__(self, player: Player, map: MapManager) -> None:
        self.player = player
        self.particles = ProceduralParticleGroup()
        self.health_bar = HealthBar(player, (64, 12), (3, 3))
        self.import_accesories()
        self.other_bars = []
    
    def import_map(self):
        self.other_bars = []

        screen_w = pygame.display.Info().current_w
        screen_h = pygame.display.Info().current_h

        for enemy in groups_picker.get_group(GroupType.Enemy).tiles():
            if enemy.type == 'snake_head': self.other_bars.append(HealthBar(enemy, (150, 12), (screen_w // 2 - 75, screen_h - 20)))

    def import_accesories(self):
        self.accesories = []
        for index, accesory in enumerate(self.player.weapon.accesories[::-1]):
            screen_w = pygame.display.Info().current_w
            screen_h = pygame.display.Info().current_h
            self.accesories.append(ModifireDisplay([self.particles], 16, (screen_w - 23 - index * 23, screen_h - 23), accesory))
    
    def update(self, dt):
        for bar in self.other_bars: bar.update(dt)
        self.health_bar.update(dt)

        for slot in self.accesories: slot.update(dt)
        self.particles.update(dt, (960, 540))
    
    def update_displayed_inventory(self):
        for item, slot in zip(self.player.weapon.accesories[::-1], self.accesories):
            slot.item = item
        
    def render(self, surf):
        for bar in self.other_bars: bar.render(surf)
        self.health_bar.render(surf)
        for index, accesory in enumerate(self.accesories): accesory.render(surf, 2 - index)
        self.particles.render(surf, pygame.Vector2(0, 0))