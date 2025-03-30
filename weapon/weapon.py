import pygame
from support.support import get_mouse_position, vector_angle
from weapon.bullet import Bullet
from cooldown.cooldown import Cooldown
from random import uniform, randint
from mouse.mouse import coursor
from tiles.tile import Tile
from particles.shoot_particle import ShootParticle
from tiles.groups_picker import *
from items.weapon_upgrade import WeaponModifire, BasicModifire

class Weapon:
    class VisualRepresentation(Tile):
        class Sprite(Tile.Sprite):
            def __init__(self, image: pygame.Surface, sort_y_offset: int, **pos: tuple[int]) -> None:
                super().__init__(image, sort_y_offset, **pos)
                self.rotated_image = image
                self.rotated_rect = self.rect
                self.scale = 1

            def update_image(self, angle, flip):
                # self.final_image = pygame.transform.flip(self.raw_image, False, True) if flip else self.raw_image
                self.transform(angle=angle, flip=(False, flip), scale=self.scale)
                # self.rotated_image = rotated_image

            def update_rect(self, mouse_vector: pygame.Vector2, rotation_point):
                render_mouse_vector = mouse_vector.copy()
                render_mouse_vector.scale_to_length(4)

                posx = rotation_point[0] + render_mouse_vector.x
                posy = rotation_point[1] + render_mouse_vector.y

                self.rotated_rect = self.final_image.get_rect(center = (posx, posy))

            def render_image(self): return self.final_image
            def render_rect(self): return self.rotated_rect

    def __init__(self, groups, assets, owner) -> None:
        self.visual_representation = self.VisualRepresentation(groups, 'weapon', assets['player']['weapon'], offgrid_tile=True, z=5, center=(0, 0))
        self.mouse_vector = pygame.Vector2()
        self.rotation_point: tuple = (0, 0)
        self.can_shoot = True
        self.owner = owner
        self.accesories = [WeaponModifire('upgrade', assets['upgrades'][0], 0), None, None]

    def shoot(self):
        accesory: BasicModifire = self.accesories[0]
        if not accesory: return
        if not self.can_shoot: return
        if self.mouse_vector.magnitude() == 0: return

        shoot_offset = self.mouse_vector.copy()
        shoot_offset.scale_to_length(10)
        pos = (self.rotation_point[0] + shoot_offset.x, self.rotation_point[1] + shoot_offset.y)

        accesory.shoot(self.mouse_vector, pos, self.accesories[2])

    def usable_ability(self):
        accesory: BasicModifire = self.accesories[1]
        if not accesory: return
        if not self.can_shoot: return
        if self.mouse_vector.magnitude() == 0: return

        shoot_offset = self.mouse_vector.copy()
        shoot_offset.scale_to_length(10)
        pos = (self.rotation_point[0] + shoot_offset.x, self.rotation_point[1] + shoot_offset.y)

        accesory.usable_ability(self.mouse_vector, pos)


    def update(self, dt: int, events, flip: bool, rotation_point: tuple):
        if events['mouse1']: self.shoot()
        if events['mouse3']: self.usable_ability()

        for accesory in self.accesories:
            if accesory: accesory.update()

        self.rotation_point = rotation_point
        self.mouse_vector = coursor.mouse_vector(rotation_point)
        if self.mouse_vector.magnitude(): self.mouse_vector.normalize_ip()
        self.visual_representation.sprite.update_image(vector_angle(self.mouse_vector), flip)
        self.visual_representation.sprite.update_rect(self.mouse_vector, self.rotation_point)


