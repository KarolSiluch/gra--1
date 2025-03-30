import pygame

from tiles.tile import Tile
from cooldown.cooldown import Cooldown
from weapon.bullet import Bullet
from tiles.groups_picker import *
from particles.shoot_particle import ShootParticle
from particles.circle import CircleParticle
from random import uniform, randint
from math import sin

class Enemy(Tile):
    def __init__(self, groups, type: str, assets, sort_y_offset: int = 0, offgrid_tile: bool = False, z=5, **pos: tuple[int]) -> None:
        super().__init__(groups, type, assets['image'], sort_y_offset, offgrid_tile, z, **pos)
        self.hitbox = self.sprite.rect.copy().inflate(-1, -1)
        self.bullet = assets['bullet']
        self.shoot_cooldown = Cooldown(1000)
        self.shake_cooldown = Cooldown(100)
        self.can_be_shot = True
        self.hp = 5
    
    def shoot(self, player_center):
        if not self.shoot_cooldown(): return

        direction = pygame.Vector2(player_center[0] - self.hitbox.centerx, player_center[1] - self.hitbox.centery)
        if 0 > direction.magnitude() > 300: return
        direction.normalize_ip()

        groups = groups_picker.get_groups(GroupType.Bullets, GroupType.Visible)

        Bullet(groups, self.bullet, direction, 450, self.type, center = self.hitbox.center)
        for _ in range(3): ShootParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.hitbox.center, direction.rotate(uniform(-15, 15)), randint(250, 350), '#964545')
        self.shoot_cooldown.reset()
    
    def get_hit(self):
        self.shake_cooldown.reset()
        self.hp = max(self.hp -1, 0)
    
    def shake(self):
        if self.shake_cooldown(): return
        offset = 2 if sin(pygame.time.get_ticks()) > 0 else 0
        self.sprite.render_offset.x = offset
    
    def update(self, dt, player_center):
        self.shoot_cooldown.timer()
        self.shake_cooldown.timer()
        self.shoot(player_center)
        self.shake()
        if self.hp == 0: self.kill()
    
    def kill(self):
        for _ in range(randint(4, 6)): ShootParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.hitbox.center, pygame.Vector2(0, 1).rotate(randint(0, 360)), randint(200, 500), 'white')
        CircleParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.hitbox.center, 30, '#d1d1d1', 100)
        return super().kill()


