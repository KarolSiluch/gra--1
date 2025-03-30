import pygame

class Potion:
    def __init__(self, type, image, restored_hp) -> None:
        self.type = type
        self.image = image
        self.restored_hp = restored_hp
    
    def interact(self, player):
        player.hp = min(player.hp + self.restored_hp, player.max_hp)
    
    def get_information(self):
        return f'will restore {self.restored_hp}hp'
