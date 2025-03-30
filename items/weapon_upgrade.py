import pygame
from weapon.bullet import Bullet
from tiles.groups_picker import *
from random import uniform, randint, choice
from particles.shoot_particle import ShootParticle
from particles.circle import CircleParticle
from cooldown.cooldown import Cooldown
from support.support import load_image
from mouse.mouse import coursor


DATA = [
    {'damage': 1, 'cooldown1': 150, 'cooldown2': 1500},
    {'damage': 1, 'cooldown1': 450, 'cooldown2': 1500},
    {'damage': 1, 'cooldown1': 200, 'cooldown2': 1500},
]

def get_modifire(assets, index):
    if index in {0}: return WeaponModifire('modifire', assets, index)
    if index in {1}: return ShotgunModifire('modifire', assets, index)
    if index in {2}: return SwordModifire('modifire', assets, index)

class BasicModifire:
    def __init__(self, type, assets, index) -> None:
        data = DATA[index]
        self.type = type
        self.image = assets['image']
        self.bullet_image = assets['bullet']
        self.damage = data['damage']
        self.shoot_cooldown = Cooldown(data['cooldown1'])
        self.ability_cooldown = Cooldown(data['cooldown2'])

        self.shoot_count = 0

    def shoot_logic(self, mouse_vector: pygame.Vector2, pos): ...

    def shoot(self, mouse_vector: pygame.Vector2, pos, passive_effect):
        if not self.shoot_cooldown(): return
        self. shoot_count += 1

        if passive_effect: passive_effect.get_effect(mouse_vector, pos, self)
        else: self.shoot_logic(mouse_vector, pos)

        self.shoot_cooldown.reset()

    def usable_ability(self, mouse_vector: pygame.Vector2, pos): ...

    def interact(self, player): player.inventory.add_item(self)

    def get_information(self): return f'adds {self.damage} damage'

    def get_effect(self, mouse_vector, pos, main_accesory): ...

    def update(self):
        self.shoot_cooldown.timer()
        self.ability_cooldown.timer()

class WeaponModifire(BasicModifire):
    def shoot_logic(self, mouse_vector: pygame.Vector2, pos):
        for _ in range(randint(2, 4)): ShootParticle(groups_picker.get_groups(GroupType.ProceduralParticles), pos, mouse_vector.rotate(uniform(-30, 30)), randint(200, 300), 'black')
        Bullet(groups_picker.get_groups(GroupType.Visible, GroupType.Bullets), self.bullet_image, mouse_vector.rotate(uniform(-2, 2)), 600, 'player', center=pos)

    def usable_ability(self, mouse_vector: pygame.Vector2, pos):
        if not self.ability_cooldown(): return
        for _ in range(randint(2, 4)): ShootParticle(groups_picker.get_groups(GroupType.ProceduralParticles), pos, mouse_vector.rotate(uniform(-30, 30)), randint(200, 300), 'white')
        self.ability_cooldown.reset()

    def get_effect(self, mouse_vector: pygame.Vector2, pos, main_accesory: BasicModifire):
        main_accesory.shoot_logic(mouse_vector, pos)

    def get_information(self):
        return f'adds {self.damage} damage'

class ShotgunModifire(BasicModifire):
    def __init__(self, type, assets, index) -> None:
        super().__init__(type, assets, index)
        self.bullets = choice([3, 5])

    def shotgun_shot(self, mouse_vector, pos, bullets):
        for index in range(1, bullets // 2 + 1):
            groups = groups_picker.get_groups(GroupType.Visible, GroupType.Bullets)

            direction = mouse_vector.rotate(5 * index)
            Bullet(groups, self.bullet_image, direction, 600, 'player', center=pos)

            direction = mouse_vector.rotate(-5 * index)
            Bullet(groups, self.bullet_image, direction, 600, 'player', center=pos)

        Bullet(groups, self.bullet_image, mouse_vector, 600, 'player', center=pos)


    def shoot_logic(self, mouse_vector, pos):
        for _ in range(randint(2, 4)): ShootParticle(groups_picker.get_groups(GroupType.ProceduralParticles), pos, mouse_vector.rotate(uniform(-30, 30)), randint(200, 300), 'black')
        self.shotgun_shot(mouse_vector, pos, self.bullets)

    def usable_ability(self, mouse_vector: pygame.Vector2, pos):
        if not self.ability_cooldown(): return
        for _ in range(randint(4, 6)): ShootParticle(groups_picker.get_groups(GroupType.ProceduralParticles), pos, mouse_vector.rotate(uniform(-30, 30)), randint(200, 300), 'white')
        self.shotgun_shot(mouse_vector, pos, 11)
        self.ability_cooldown.reset()

    def get_information(self):
        return f'shothun with {self.bullets} bullets'

    def get_effect(self, mouse_vector, pos, main_accesory: BasicModifire):
        groups = groups_picker.get_groups(GroupType.Visible, GroupType.Bullets)
        if main_accesory.shoot_count % 5 == 0:
            for index in range(-1, 2):
                direction = mouse_vector.rotate(5 * index)
                Bullet(groups, main_accesory.bullet_image, direction, 600, 'player', center=pos)

        else: main_accesory.shoot_logic(mouse_vector, pos)

class SwordModifire(BasicModifire):
    def shoot_logic(self, mouse_vector: pygame.Vector2, pos):
        groups = groups_picker.get_groups(GroupType.Visible, GroupType.Bullets)

        offset = mouse_vector.rotate(180 + randint(-70, 70))
        offset.scale_to_length(30)

        pos_x = pos[0] + offset.x
        pos_y = pos[1] + offset.y

        mpos_x, mpos_y = coursor.get_pos()
        direction = pygame.Vector2(mpos_x - pos_x, mpos_y - pos_y).normalize()

        Bullet(groups, self.bullet_image, direction, 600, 'player', center = (pos_x, pos_y))
        CircleParticle(groups_picker.get_groups(GroupType.ProceduralParticles), (pos_x, pos_y), 4, '#ffe380', 30)

    def get_effect(self, mouse_vector, pos, main_accesory: BasicModifire):
        main_accesory.shoot_logic(mouse_vector, pos)
        self.shoot_logic(mouse_vector, pos)



