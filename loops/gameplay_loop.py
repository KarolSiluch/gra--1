import pygame
from gameplay import Gameplay


class GameplayLoop:
    def __init__(self, game) -> None:
        self._game = game
        self._gameplay = Gameplay()
        self.reset_events()

    @property
    def gameplay(self):
        return self._gameplay

    def enter(self):
        self.reset_events()
        self._gameplay.ui.update_displayed_inventory()

    def exit(self): ...

    def reset_events(self):
        self._events: dict[str, bool] = {'w': False, 'a': False, 's': False, 'd': False, 'e': False,
                                         'mouse1': False, 'mouse3': False, 'shift': False, 'q': False}

    def update(self, dt):
        self._gameplay.update(dt, self._events)
        self._events['e'] = False
        self._events['mouse3'] = False

    def render(self, display: pygame.Surface):
        display.fill('#151023')
        self._gameplay.render(display)

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self._events['w'] = True
                if event.key == pygame.K_a:
                    self._events['a'] = True
                if event.key == pygame.K_s:
                    self._events['s'] = True
                if event.key == pygame.K_d:
                    self._events['d'] = True
                if event.key == pygame.K_LSHIFT:
                    self._events['shift'] = True
                if event.key == pygame.K_e:
                    self._events['e'] = True
                if event.key == pygame.K_q:
                    self._events['q'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self._events['w'] = False
                if event.key == pygame.K_a:
                    self._events['a'] = False
                if event.key == pygame.K_s:
                    self._events['s'] = False
                if event.key == pygame.K_d:
                    self._events['d'] = False
                if event.key == pygame.K_LSHIFT:
                    self._events['shift'] = False
                if event.key == pygame.K_q:
                    self._events['q'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._events['mouse1'] = True
                if event.button == 3:
                    self._events['mouse3'] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self._events['mouse1'] = False

    def next_loop(self):
        if self._events['q']:
            return 'inventory'
