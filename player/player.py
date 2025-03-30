import pygame
from weapon.weapon import Weapon
from tiles.tile import Tile
from tiles.animated_tile import AnimatedTile
from mouse.mouse import coursor
from tiles.tilemap import TileMap
from tiles.groups_picker import *
from states.state_machine import StateMachine
from player.inventory import Inventory
from cooldown.cooldown import Cooldown

class Player(AnimatedTile):
    class Sprite(AnimatedTile.Sprite):
        def render_image(self):
            mouse_x, _ = coursor.get_pos()
            self.flip = False
            if self.rect.centerx > mouse_x:self.flip = True
            self.transform(angle=self.angle, flip=(self.flip , False))

            return self.final_image
        

    def __init__(self, groups, assets, **pos: tuple[int]) -> None:
        self.state_machine = StateMachine(self)
        super().__init__(groups, 'player', assets['player']['animations'], self.state_machine.state, offgrid_tile=True, **pos)
        self.shadow = Tile(groups_picker.get_groups(GroupType.Visible), 'shadow', assets['player']['shadow'], sort_y_offset=-self.sprite.rect.height, offgrid_tile=True, midbottom=self.sprite.rect.midbottom)
        self.shadow.sprite.raw_image.set_alpha(200)
        self.weapon = Weapon(groups_picker.get_groups(GroupType.Visible), assets, self.type)

        self.inventory = Inventory((5, 5))

        self.immunity_frames = Cooldown(400)

        self.max_hp = 50
        self.hp = self.max_hp

        self.can_be_shot = True
        self.using_e = False
    
    def add_to_new_group(self):
        self.kill()
        self.weapon.visual_representation.kill()
        self.shadow.kill()
        self.__add_to_groups__(groups_picker.get_groups(GroupType.Visible, GroupType.HitableEntities), True)
        self.weapon.visual_representation.__add_to_groups__(groups_picker.get_groups(GroupType.Visible), True)
        self.shadow.__add_to_groups__(groups_picker.get_groups(GroupType.Visible), True)
    
    def contact_damage(self, damage, direction):
        if not self.can_be_shot: return
        if not self.immunity_frames: return
        self.state_machine.change_state('contact_damage')
        if not self.state_machine.state == 'contact_damage': return

        print(pygame.time.get_ticks())

        self.state_machine.current_state.pass_information(direction)
        self.hp = max(self.hp - damage, 0)
        self.immunity_frames.reset()
            
    def get_hit(self):
        if not self.immunity_frames(): return
        self.hp = max(self.hp - 4, 0)
        self.immunity_frames.reset()
    
    def get_direction(self, events):
        self.direction = pygame.Vector2(events['d'] - events['a'], events['s'] - events['w'])
        if self.direction.magnitude(): self.direction = self.direction.normalize()
    
    def interact(self, activatable_tiles: TileMap):
        tiles = activatable_tiles.grid_tiles_around(self.hitbox.center)
        for tile in tiles:
            if not self.hitbox.colliderect(tile.activation_trigger): continue
            tile.interact(self)
    
    def update(self, dt, events, map):
        self.immunity_frames.timer()

        self.using_e = events['e']
        self.get_direction(events)
        self.state_machine.update(dt, events, map.sprite_groups[GroupType.Collidable])

        self.interact(map.sprite_groups[GroupType.Activitable])
        self.animate()
        
        weapon_offset_x = 1 if self.sprite.flip else -1
        self.weapon.update(dt, events, self.sprite.flip, (self.hitbox.centerx + weapon_offset_x + self.sprite.render_offset.x, self.hitbox.centery + self.sprite.render_offset.y + 4))
        self.weapon.visual_representation.sprite.rect.bottom = self.sprite.rect.bottom + 5
        self.shadow.sprite.rect.center = (self.hitbox.centerx, self.hitbox.centery + self.sprite.raw_image.height / 2)