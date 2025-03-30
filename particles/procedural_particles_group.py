import pygame
from particles.shoot_particle import ShootParticle
from tiles.tilemap import TileMap

class ProceduralParticleGroup(TileMap):
    def tiles(self) -> list[ShootParticle]: return super().tiles()

    def render(self, display: pygame.Surface, camera_offset: pygame.Vector2):
        for particle in self.tiles(): particle.render(display, camera_offset)

