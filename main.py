import pygame
# Używam pygame-ce (nie zadziała ze zwykłym pygame)
import time
from loops.gameplay_loop import GameplayLoop
from loops.inventory_loop import InventoryLoop


def Render_Text(screen: pygame.Surface, what: str, color, where):
    font = pygame.font.Font(None, 30)
    text = font.render(what, True, pygame.Color(color))
    screen.blit(text, where)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self._running: bool = True
        self._clock: pygame.Clock = pygame.time.Clock()
        self._previous_time = time.time()

        screen_size: list[int] = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        flags = pygame.FULLSCREEN | pygame.SCALED
        self._screen: pygame. Surface = pygame.display.set_mode((screen_size[0] // 3, screen_size[1] // 3), flags)
        self.loops = {
            'gameplay': GameplayLoop(self),
            'inventory': InventoryLoop(self)
        }
        self._current_loop = self.loops['gameplay']

    def close(self):
        self._running = False

    def change_state(self, loop: str):
        if not loop:
            return
        self._current_loop.exit()
        self._current_loop = self.loops[loop]
        self._current_loop.enter()

    def main_loop(self):
        while self._running:
            self._clock.tick()
            dt = time.time() - self._previous_time
            self._previous_time = time.time()
            self._current_loop.get_events()
            self.change_state(self._current_loop.next_loop())
            self._current_loop.update(dt)
            self._current_loop.render(self._screen)
            Render_Text(self._screen, str(int(self._clock.get_fps())), (255, 0, 0), (self._screen.width - 40, 3))
            pygame.display.update()


if __name__ == '__main__':
    Game().main_loop()
