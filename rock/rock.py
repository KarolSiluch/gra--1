import pygame
from tiles.outlined_tile import OutlinedTile
from particles.circle import CircleParticle
from particles.board import Board
from tiles.groups_picker import *
from random import randint
from mobs.spawner import MobSpawner
from rock.states.state_machine import StateMachine

class Rock(OutlinedTile):
    def __init__(self, groups, type: str, image: pygame.Surface, game, stage, sort_y_offset: int = 0, offgrid_tile: bool = False, z=5, **pos: tuple[int]) -> None:
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, z, **pos)
        self.active = False
        self.game = game
        self.stage = stage
        self.state_machine = StateMachine(self, game, stage)
        self.resorce = 0
        self.board = Board(groups_picker.get_groups(GroupType.ProceduralParticles), 'board', (self.hitbox.centerx, self.hitbox.top - 7), (30, 20))
        self.waves = randint(2, 2)
        self.current_wave = 1
    
    def interact(self, player): self.state_machine.interact(player)
        # if self.active: return
        # self.active = True

    # def spawn(self):
    #     if not self.active: return
    #     if self.particle.radius < 50: return
    #     if self.particle.radius == self.particle.max_radius: return
    #     if randint(0, 10): return

    #     spawner: MobSpawner = self.map.sprite_groups[GroupType.Enemy]
    #     assets = self.map.game.assets['enemy']
    #     spawn_offset = pygame.Vector2(0, self.particle.radius).rotate(randint(0, 360))
    #     pos = (self.hitbox.centerx + spawn_offset.x, self.hitbox.centery + spawn_offset.y)

    #     enemy = spawner.spawn_enemy(self.map.sprite_groups[GroupType.Collidable], assets, pos)
    #     if enemy: self.enemies.append(enemy)
    
    def spawn_resorce(self, amount):
        self.resorce += amount
    
    def update(self, dt):
        self.state_machine.update(dt)
        # self.spawn()
        # self.spawn_resorce()
        

        

    
