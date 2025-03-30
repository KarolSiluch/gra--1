import pygame
from random import randint, choice
from math import sin, cos, radians
from tiles.tile import Tile


class GrassManages:
    def __init__(self, cell_size: int) -> None:
        self.cell_size: int = cell_size
        self.grid: dict[tuple[int], list[Grass]] = {}
        self.wind = 0

    def spawn_grass(self, groups, assets: list[pygame.Surface], cords: tuple[int], amount_of_grass_blades: int) -> None:
        offset_x, offset_y = cords[0] * self.cell_size, cords[1] * self.cell_size
        if not cords in self.grid.keys(): self.grid[cords] = []
        for _ in range(amount_of_grass_blades):
            x, y = offset_x + randint(0, self.cell_size), offset_y + randint(0, self.cell_size)
            image = choice(assets)
            self.grid[cords].append(Grass(groups, image, self.cell_size, midbottom=(x, y)))

    def render(self, display: pygame.Surface):
        for gras_blades in self.grid.values():
            for grass_blade in gras_blades:
                grass_blade.render(display, pygame.Vector2(0, 0))

    def grid_tiles_around(self, point: tuple[float], radius: int = 1):
        x_index = int(point[0] / self.cell_size)
        y_index = int(point[1] / self.cell_size)

        tiles = []

        for y_offset in range(-radius, radius + 1):
            for x_offset in range(-radius, radius + 1):
                x, y = x_index + x_offset, y_index + y_offset
                if not (x, y) in self.grid.keys():
                    continue
                tiles.extend(self.grid[(x, y)])
        return tiles

    def blades_number(self):
        x = 0
        for grass_blades in self.grid.values():
            x += len(grass_blades)
        return x

    def update(self, dt, player_center):
        self.wind += dt * 2
        for grass_blade in self.grid_tiles_around(player_center, 17):
            grass_blade.update(self.wind)


class Grass(Tile):
    class Sprite(Tile.Sprite):
        cached_images = {}

        def __init__(self, image: pygame.Surface, sort_y_offset: int, **pos: tuple[int]) -> None:
                self.show = True
                self.image = image
                self.rect: pygame.FRect = image.get_rect(**pos)
                self.sort_y_offset = sort_y_offset
                self.render_offset = pygame.Vector2()

        def render_image(self, angle): return self.cached_images[(self.image, angle)]

        def render_rect(self, angle):
            rotated_image: pygame.Surface = self.cached_images[(self.image, angle)]
            half_of_the_width = self.image.get_width() // 2
            if 0 < angle < 90:
                render_rect = rotated_image.get_rect(bottomleft = self.rect.midbottom)
                direction = 1
            else:
                render_rect = rotated_image.get_rect(bottomright = self.rect.midbottom)
                direction = -1
            angle_radius: float = radians(angle)
            offset = pygame.Vector2(-sin(angle_radius) * half_of_the_width, cos(angle_radius) * half_of_the_width)
            render_rect.center += direction * offset
            return render_rect

        def update_image(self, angle):
            cache_lookup = (self.image, angle)

            if not (cached_image := self.cached_images.get(cache_lookup, None)):
                cached_image = pygame.transform.rotate(self.image, angle - 90)
                self.cached_images[cache_lookup] = cached_image

    def __init__(self, groups, image: pygame.Surface, cell_size: int, **pos: tuple[int]) -> None:
        super().__init__(groups, 'grass', image, **pos)
        self.angle = 0
        self.col = self.sprite.rect.centerx // cell_size

    def get_sprite(self):
        self.sprite.update_image(self.angle)
        return (self.sprite.render_image(self.angle), self.sprite.render_rect(self.angle))

    def update(self, wind):
        self.angle = int(90 + sin(wind + self.col * 0.1) * 20)
