import pygame

class InGameMouse:
    def __init__(self) -> None:
        self.coursor = pygame.Vector2()
        
    def update(self, offset: pygame.Vector2) -> tuple:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.coursor = pygame.Vector2(offset.x + mouse_x, offset.y + mouse_y)
    
    def mouse_vector(self, point):
        point_x, point_y = point
        return pygame.Vector2(self.coursor.x - point_x, self.coursor.y - point_y)
    
    def get_pos(self):
        return tuple(self.coursor)

coursor = InGameMouse()
        