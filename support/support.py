import pygame

def load_image(path: str):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (image.get_width() * 1, image.get_height() * 1))

def import_cut_graphics(number_of_tiles: tuple[int], path: str) -> list[pygame.Surface]:
    images = []
    surface = load_image(path)
    image_width = surface.get_width() // number_of_tiles[0]
    image_height = surface.get_height() // number_of_tiles[1]
    for row in range(number_of_tiles[1]):
        for col in range(number_of_tiles[0]):
            new_surfece = pygame.Surface((image_width, image_height), flags=pygame.SRCALPHA)
            offset = (-col * image_width, -row * image_height)
            new_surfece.blit(surface, offset)
            images.append(new_surfece)
    return images

def get_mouse_position() -> tuple:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return (mouse_x, mouse_y)

def vector_angle(vector: pygame.Vector2):
    return vector.angle_to(pygame.Vector2(1, 0))
    
    