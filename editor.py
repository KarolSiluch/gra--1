import pygame
import time
from support.support import load_image, import_cut_graphics
from map_editor.editor_mapmanager import EditorMapManager
from mouse.mouse import coursor
from map_editor.editor_tile import EditorTile


class Editor:
    def __init__(self) -> None:
        pygame.init()
        self.running: bool = True
        self.clock: pygame.Clock = pygame.time.Clock()
        self.previous_time = time.time()
        self.events: dict[str, bool] = {'w': False, 'a': False, 's': False, 'd': False, 'mouse1': False, 'mouse3': False, 'shift': False}

        screen_size: list[int] = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen: pygame.Surface = pygame.display.set_mode((screen_size[0] // 3, screen_size[1] // 3), pygame.FULLSCREEN | pygame.SCALED)

        self.import_assets()
        self.camera_offset = pygame.Vector2(20, 0)
        self.tile_size = 16
        self.map_manager = EditorMapManager(self, self.tile_size)

        self.tile_list = self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.off_grid = False
        
    def update(self, dt):
        self.camera_offset.x += (self.events['d'] - self.events['a']) * 200 * dt
        self.camera_offset.y += (self.events['s'] - self.events['w']) * 200 * dt
        self.map_manager.update(dt)

    def edition_stuff(self):
        type = self.tile_list[self.tile_group]
        current_tile = self.assets[type][self.tile_variant].copy()
        current_tile.set_alpha(200)
        self.screen.blit(current_tile, (20, 20))

        mpos =  pygame.mouse.get_pos()
        mouse_x, mouse_y = mpos[0], mpos[1]
        if type == 'pine_tree':
            render_rect = current_tile.get_rect(midbottom = (mouse_x, mouse_y))
            self.screen.blit(current_tile, render_rect)
        
        if type == 'player':
            render_rect = current_tile.get_rect(center = (mouse_x, mouse_y))
            self.screen.blit(current_tile, render_rect)

        elif self.off_grid:
            self.screen.blit(current_tile, (mouse_x, mouse_y))

        else:
            x = ((mouse_x + self.camera_offset.x) // self.tile_size) * self.tile_size - self.camera_offset.x 
            y = ((mouse_y + self.camera_offset.y) // self.tile_size) * self.tile_size - self.camera_offset.y
            self.screen.blit(current_tile, (x, y))
        
        
    def render(self):
        self.screen.fill('#323c39')
        self.map_manager.render(self.screen)
        self.edition_stuff()

        for y_offset in range(0, self.screen.height, self.tile_size):
            y = y_offset - self.camera_offset.y % self.tile_size
            pygame.draw.line(self.screen, 'black', (0, y), (self.screen.width, y))
        for x_offset in range(0, self.screen.width, self.tile_size):
            x = x_offset - self.camera_offset.x % self.tile_size
            pygame.draw.line(self.screen, 'black', (x, 0), (x, self.screen.height))
        
        pygame.display.update()
    
    def add_tile(self):
        ingame_mpos = coursor.get_pos()

        type = self.tile_list[self.tile_group]
        image = self.assets[type][self.tile_variant]
        
        layer = 5
        if type == 'pine_tree':
            if not self.off_grid: return
            pos = {'midbottom': ingame_mpos}
            layer = 6
        
        if type == 'player':
            if not self.off_grid: return
            pos = {'center': ingame_mpos}

        elif self.off_grid: pos = {'topleft': ingame_mpos}

        else:
            if type == 'floor': layer = 0
            index_x = (ingame_mpos[0] // self.tile_size) 
            index_y = (ingame_mpos[1] // self.tile_size)
            pos = {'topleft': (index_x * self.tile_size, index_y * self.tile_size)}

        # if (index_x, index_y) in self.map_manager.sprite_group.tile_map.keys(): return
        EditorTile([self.map_manager.sprite_group], type, self.tile_variant, image, offgrid_tile=self.off_grid, z=layer, **pos)
    
    def remove_tile(self):
        ingame_mpos = coursor.get_pos()

        collision_tiles = []
        for tile in self.map_manager.sprite_group.offgrid_tiles:
            if tile.type == 'background': continue
            if not tile.sprite.rect.collidepoint(ingame_mpos): continue
            collision_tiles.append(tile)
        if len(collision_tiles):
            collision_tiles[-1].kill()
            return

        if len(tiles :=self.map_manager.sprite_group.grid_tiles_around(ingame_mpos, 0)): tiles[-1].kill()

    def main_loop(self):
        fps = 0
        frame = 0
        while self.running:
            self.clock.tick()
            fps += self.clock.get_fps()
            frame += 1
            dt = time.time() - self.previous_time
            self.previous_time = time.time()
            self.get_events()
            self.update(dt)
            self.render()
        print(fps / frame)
    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: self.events['w'] = True
                if event.key == pygame.K_a: self.events['a'] = True
                if event.key == pygame.K_s: self.events['s'] = True
                if event.key == pygame.K_d: self.events['d'] = True
                if event.key == pygame.K_LSHIFT: self.events['shift'] = True
                if event.key == pygame.K_g: self.off_grid = not self.off_grid
                if event.key == pygame.K_o: self.map_manager.save('map2.json')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w: self.events['w'] = False
                if event.key == pygame.K_a: self.events['a'] = False
                if event.key == pygame.K_s: self.events['s'] = False
                if event.key == pygame.K_d: self.events['d'] = False
                if event.key == pygame.K_LSHIFT: self.events['shift'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.add_tile()
                    self.events['mouse1'] = True
                if event.button == 3:
                    self.remove_tile()
                    self.events['mouse3'] = True
                if event.button == 4:
                    if self.events['shift']:
                        self.tile_variant = 0
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                    else: self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                if event.button == 5:
                    if self.events['shift']:
                        self.tile_variant = 0
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                    else: self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: self.events['mouse1'] = False
                if event.button == 3: self.events['mouse3'] = False

    def import_assets(self):
        self.assets = {
            'wall': import_cut_graphics((3, 4), 'assets/walls.png'),
            'lab_wall': import_cut_graphics((1, 2), 'assets/tiles/lab_wall.png'),
            'pine_tree': [load_image('assets/trees/pine_tree_editor.png')],
            'grass': [load_image('assets/grass/grass_editor.png')],
            'rock': [load_image('assets/spawner/rock.png')],
            'player': [load_image('assets/player/Accelerator.png')],
            'border': [load_image('assets/map1/Border.png')],

        }
                
if __name__ == '__main__':
    Editor().main_loop()