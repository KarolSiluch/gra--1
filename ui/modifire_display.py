import pygame

from inventory.inventory import InventorySlot

class ModifireDisplay(InventorySlot):
    def __init__(self, groups, slot_size, pos, item) -> None:
        super().__init__(groups, slot_size, pos, item)
        self.cooldown_color = (50, 50, 50)
        # self.cooldown_color = 'black'

    def render(self, display: pygame.Surface, index):
        self.surface.fill(self.color)
        if self.item:
            self.surface.blit(self.item.image, (1, 1))
            if index == 0: multiplier = max(0, 1 - (pygame.time.get_ticks() - self.item.shoot_cooldown.last_used_time) / self.item.shoot_cooldown.time_long)
            elif index == 1: multiplier = max(0, 1 - (pygame.time.get_ticks() - self.item.ability_cooldown.last_used_time) / self.item.ability_cooldown.time_long)
            elif index == 2: multiplier = 0
            cooldown_surface = pygame.Surface((self.rect.width, int(self.rect.height * multiplier)))
            cooldown_surface.fill(self.cooldown_color)
            cooldown_rect = cooldown_surface.get_rect(bottomleft = (0, self.rect.height))
            self.surface.blit(cooldown_surface, cooldown_rect, special_flags=pygame.BLEND_RGB_MIN)
        display.blit(self.surface, self.rect)


        