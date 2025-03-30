import pygame
from inventory.inventory import Inventory


class InventoryLoop:
    def __init__(self, game) -> None:
        self._game = game
        self.reset_events()
        self._inventory = Inventory()

    def enter(self):
        self.reset_events()
        self._inventory.import_inventory(self._game.loops['gameplay'].gameplay.player)

    def exit(self): self._inventory.load_inventory()

    def reset_events(self): self._events: dict[str, bool] = {'q': False, 'mouse1': False}

    def update(self, dt): self._inventory.update(dt)

    def render(self, display: pygame.Surface):
        display.fill('#222034')
        self._inventory.render(display)

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self._events['q'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self._events['q'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._events['mouse1'] = True
                self._inventory.use_mouse()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self._events['mouse1'] = False

    def next_loop(self):
        if self._events['q']:
            return 'gameplay'
