import pygame


class Inventory:
    def __init__(self, size: tuple[int]) -> None:
        self.size_x, self.size_y = size
        self.inventory_space = {}
    
    def add_item(self, item):
        for y in range(self.size_y):
            for x in range(self.size_x):
                pos = (x, y)
                if pos in self.inventory_space.keys(): continue
                self.inventory_space[pos] = item
                print(self.inventory_space)

                return True
        return False