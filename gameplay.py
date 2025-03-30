import pygame
from player.player import Player
from grass import GrassManages
from support.support import import_cut_graphics, load_image
from tiles.mapmanager import MapManager
from mouse.mouse import InGameMouse
from tiles.groups_picker import *
from ui.ui import UserInterface
from animation.animation import Animation, SetAnimation

class Gameplay:
    def __init__(self) -> None:
        self.import_assets()
        
        self.stage = 0
        self.lobby = MapManager(self, 16, 'map', self.stage)
        # self.current_map = MapManager(self, 16, 'map2', self.stage)
        self.current_map = self.lobby
        self.transiton = Transition(self)

        self.player: Player = Player(groups_picker.get_groups(GroupType.Visible, GroupType.HitableEntities), self.assets, center=self.current_map.player_start_position)

        self.ui = UserInterface(self.player, self.current_map)
    
    def next_stage(self): self.stage += 1

    def new_map(self, map): self.transiton.new_map(map)

    def import_map(self, map):
        if map == 'lobby':
            self.stage = 0
            self.current_map = self.current_map = self.lobby
            self.current_map.enter()
            self.player.hp = self.player.max_hp
        else:
            self.current_map = MapManager(self, 16, map, self.stage)
        
        self.ui.import_map()
        self.player.hitbox.center = self.current_map.player_start_position
        self.player.sprite.rect.center = self.current_map.player_start_position
        self.player.add_to_new_group()
    
    def update(self, dt: float, events: dict[str, bool]) -> None:
        self.transiton.update(dt)
        self.player.update(dt, events, self.current_map)
        self.current_map.update(dt)
        self.ui.update(dt)

        if self.player.hp > 0: return
        if self.transiton.next_map: return
        self.new_map('lobby')
            
    
    def render(self, display):
        self.current_map.render(display)
        self.ui.render(display)
        self.transiton.render(display)
    
    def import_assets(self):
        self.assets = {
            'player': {
                'animations': {
                    'idle': Animation(import_cut_graphics((5, 1), 'assets/player/idle.png'), animation_speed=7),
                    'run': Animation(import_cut_graphics((4, 1), 'assets/player/run.png'), animation_speed=10),
                    'dodge': SetAnimation(import_cut_graphics((4, 1), 'assets/player/dodge.png'))
                    },
                'shadow': load_image('assets/player/shadow.png'),
                'weapon': load_image('assets/weapons/ak.png')
                },
            
            'boss': import_cut_graphics((1, 3), 'assets/spawner/boss/0.png'),
            
            'wall': import_cut_graphics((3, 4), 'assets/walls.png'),
            'lab_wall': import_cut_graphics((1, 2), 'assets/tiles/lab_wall.png'),
            'pine_tree': import_cut_graphics((1, 4), 'assets/trees/pine_tree.png'),
            'grass': import_cut_graphics((3, 1), 'assets/grass2.png'),
            'rock': [load_image('assets/spawner/rock.png')],
            'shadows': import_cut_graphics((11, 1), 'assets/map1/shadows.png'),

            'enemy': {'image': load_image('assets/spawner/enemy1/0.png'),
                      'bullet': load_image('assets/spawner/enemy1/1.png')},

            'potion': [load_image('assets/items/potion.png')],

            'background': {
                'map': load_image('assets/map1/background.png'),
                'map2': load_image('assets/map2/background.png'),
                'map3': load_image('assets/map3/background.png')},

            'upgrades': [
                {'image': load_image('assets/items/0.png'), 'bullet': load_image('assets/weapons/bullet.png')},
                {'image': load_image('assets/items/1.png'), 'bullet': load_image('assets/weapons/1.png')},
                {'image': load_image('assets/items/2.png'), 'bullet': load_image('assets/weapons/2.png')},
            ],
        }

class Transition:
    def __init__(self, game: Gameplay):
        self.game = game
        self.transition = 320
        self.next_map = None

    def new_map(self, map):
        self.next_map = map
        self.transition = -320
    
    def update(self, dt):
        self.transition = min(self.transition + dt * 500, 320)
        if self.next_map:
            if self.transition > 0:
                self.game.import_map(self.next_map)
                self.next_map = None
        
    def render(self, display: pygame.Surface):
        if self.transition < 320:
            transition_surface = pygame.Surface(display.get_size())
            pygame.draw.circle(transition_surface, 'white', (display.get_width() // 2, display.get_height() // 2), abs(self.transition))
            transition_surface.set_colorkey('white')
            display.blit(transition_surface, (0, 0))
