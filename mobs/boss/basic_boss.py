import pygame
from player.player import Player
from tiles.tile import Entity
from tiles.groups_picker import *
from math import copysign
from support.support import vector_angle
from particles.shoot_particle import ShootParticle
from particles.circle import CircleParticle
from random import randint

class Snake:
    def __init__(self, groups, type: str, assets, sort_y_offset: int = 0, offgrid_tile: bool = False, **pos: tuple[int]) -> None:
        self.type = type
        self.head = SnakeHead(groups, assets, sort_y_offset, offgrid_tile, **pos)
        
    def is_alive(self):
        return self.head.alive

class SnakePart(Entity):
    class Sprite(Entity.Sprite):
        def render_image(self):
            self.transform(angle=self.angle, flip=(self.flip , False))

            return self.final_image
    
    def __init__(self, groups, type: str, image: pygame.Surface, sort_y_offset: int = 0, offgrid_tile: bool = False, **pos: tuple[int]) -> None:
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, **pos)
        self.next_part = None
        self.can_be_shot = True
        self.damage_dealt = 0
    
    def get_hp(self):
        if not self.next_part: return self.damage_dealt
        return self.damage_dealt + self.next_part.get_hp()

    def get_hit(self): 
        self.damage_dealt += 1
        # print(self.damage_dealt)

    def contact_damage(self, player: Player):
        if not self.hitbox.colliderect(player.hitbox): return
        player_vector = pygame.Vector2(player.hitbox.centerx - self.hitbox.centerx, player.hitbox.centery - self.hitbox.centery)
        if player_vector.magnitude(): player_vector.normalize_ip()
        player.contact_damage(10, player_vector)
        # print('nigger1', self.damage_dealt)
    
    def create_snake(self, index: int, type: str, assets, sort_y_offset: int = 0, offgrid_tile: bool = False, **pos: tuple[int]):
        if index == 0: return
        image = assets[2] if index == 1 else assets[1]
        self.next_part = SnakePart(groups_picker.get_groups(GroupType.Visible, GroupType.HitableEntities, GroupType.ContactDamage), type, image, sort_y_offset, offgrid_tile, **pos)
        self.next_part.create_snake(index - 1, type, assets, sort_y_offset, offgrid_tile, **pos)

    def update(self, dt):
        if self.next_part:
            self.next_part.update(dt)
            segment_vector = pygame.Vector2(self.next_part.hitbox.centerx - self.hitbox.centerx, self.next_part.hitbox.centery - self.hitbox.centery)
            self.next_part.sprite.angle = vector_angle(segment_vector) + 90

            if segment_vector.magnitude():
                segment_vector.scale_to_length(min(segment_vector.magnitude(), 25))
                self.next_part.hitbox.center = self.hitbox.center + segment_vector
                self.next_part.sprite.rect.center = self.hitbox.center + segment_vector
    
    def kill(self):
        if self.next_part: self.next_part.kill()
        for _ in range(10): ShootParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.hitbox.center, pygame.Vector2(0, 1).rotate(randint(0, 360)), randint(200, 500), '#3c2040')
        CircleParticle(groups_picker.get_groups(GroupType.ProceduralParticles), self.hitbox.center, 40, '#151023', 150)
        super().kill()

class SnakeHead(SnakePart):
    def __init__(self, groups, assets, sort_y_offset: int = 0, offgrid_tile: bool = False, **pos: tuple[int]) -> None:
        super().__init__(groups, 'snake_head', assets[0], sort_y_offset, offgrid_tile, **pos)
        self.player_vector = pygame.Vector2()
        self.direction = pygame.Vector2(0, -1)
        self.velocity = 600
        self.create_snake(30, 'snake_body', assets, offgrid_tile=True, **pos)
        self.active = False

        self.alive = True

        self.max_hp = 400
        self.hp = self.max_hp
    
    def contact_damage(self, player: Player):
        if not self.hitbox.colliderect(player.hitbox): return
        player_vector = pygame.Vector2(player.hitbox.centerx - self.hitbox.centerx, player.hitbox.centery - self.hitbox.centery)
        if player_vector.magnitude(): player_vector.normalize_ip()
        player.contact_damage(20, player_vector)
    
    def move(self, dt, player_center):
        self.player_vector = pygame.Vector2(player_center[0] - self.hitbox.centerx, player_center[1] - self.hitbox.centery)

        if self.active:
            if self.player_vector.magnitude() > 50:
                angle = self.player_vector.angle_to(self.direction)
                self.direction.rotate_ip(abs(angle) * dt * 3)
                self.sprite.angle = vector_angle(self.direction) - 90

            self.hitbox.centerx += self.direction.x * self.velocity * dt
            self.hitbox.centery += self.direction.y * self.velocity * dt
            self.sprite.rect.center = self.hitbox.center

            super().update(dt)
        else:
            if self.player_vector.magnitude() < 100: self.active = True

    
    def update(self, dt, player_center):
        self.move(dt, player_center)

        if self.alive:
            self.hp = self.max_hp - self.get_hp()
            self.alive = self.hp > 0
            if not self.alive: self.kill()

        




    