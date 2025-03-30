import pygame
from player.inventory import Inventory as PlayerInventory
from particles.procedural_particles_group import ProceduralParticleGroup
from particles.board import Board
from player.player import Player
from items.weapon_upgrade import BasicModifire

class Inventory:
    def __init__(self) -> None:
        self.slot_size = 16
        self.coursor = InventoryCoursor()
        self.particles = ProceduralParticleGroup(16)
        self.lines_offset = 0
    
    def use_mouse(self):
        mpos = self.coursor.get_pos()
        for slot in self.all_slots():
            if not slot.rect.collidepoint(mpos): continue
            self.coursor.held_item, slot.item = slot.item, self.coursor.held_item

            # if self.coursor.held_item:
            #     if slot.item: continue
            #     slot.item = self.coursor.held_item
            #     self.coursor.held_item = None
            # else:
            #     if not slot.item: continue
            #     self.coursor.held_item = slot.item
            #     slot.item = None
                
    
    def import_inventory(self, player: Player):
        self.player = player
        self.slots = []
        self.weapon_slots = []

        for index, accesorie in enumerate(self.player.weapon.accesories):
            posy = index * (self.slot_size + 7) + 100
            self.weapon_slots.append(InventorySlot([self.particles], self.slot_size, (300, posy), accesorie))

        for y in range(player.inventory.size_y):
            for x in range(player.inventory.size_x):
                posx = x * (self.slot_size + 7) + 175
                posy = y * (self.slot_size + 7) + 75

                item = None
                if (x, y) in player.inventory.inventory_space.keys():
                    item = player.inventory.inventory_space[(x, y)]        

                self.slots.append(InventorySlot([self.particles], self.slot_size, (posx, posy), item))
        
    def all_slots(self):
        slots = self.slots.copy()
        slots.extend(self.weapon_slots)
        return slots
    
    def load_inventory(self):
        inventory = {}
        for index, slot in enumerate(self.slots):
            if not slot.item: continue
            y = index // self.player.inventory.size_x
            x = index % self.player.inventory.size_x
            inventory[(x, y)] = slot.item
        self.player.inventory.inventory_space = inventory

        accesories = []
        for accesorie in self.weapon_slots: accesories.append(accesorie.item if accesorie.item else None)
        self.player.weapon.accesories = accesories

    def update(self, dt):
        self.lines_offset += dt * 30
        for slot in self.all_slots(): slot.update(dt)
        self.particles.update(dt, (960, 540))
    
    def draw_lines(self, display: pygame.Surface):
        for x_offset in range(-180, display.get_width() + 180, 30):
            pygame.draw.line(display, '#050111', (x_offset + self.lines_offset % 90, 0), (x_offset + self.lines_offset % 90 + 90, display.get_height()), 7)

    def render(self, display: pygame.Surface):
        self.draw_lines(display)
        for slot in self.all_slots(): slot.render(display)
        self.particles.render(display, pygame.Vector2(0, 0))
        self.coursor.render(display)


class InventorySlot:
    def __init__(self, groups, slot_size, pos, item: BasicModifire) -> None:
        self.surface = pygame.Surface((slot_size + 2, slot_size + 2))
        self.rect = self.surface.get_frect(topleft = pos)
        self.item = item
        self.board = Board(groups, 'board', (self.rect.centerx, self.rect.top - 1), (70, 16))
        self.color = '#85898f'
    
    def update(self, dt):
        mpos = pygame.mouse.get_pos()
        self.color = '#50535d'
        if self.rect.collidepoint(mpos):
            self.color = '#85898f'
            if self.item:
                self.board.show(self.item.get_information())
    
    def render(self, display: pygame.Surface):
        self.surface.fill(self.color)
        if self.item: self.surface.blit(self.item.image, (1, 1))
        display.blit(self.surface, self.rect)

class InventoryCoursor:
    def __init__(self) -> None:
        self.held_item = None
        self.taken_from = None
    
    def get_pos(self):
        return pygame.mouse.get_pos()

    def render(self, display: pygame.Surface):
        if not self.held_item: return
        rect = self.held_item.image.get_rect(center = self.get_pos())
        display.blit(self.held_item.image, rect)
