from .overlay import Overlay
from menu import Button
import colors
from stgs import winWidth, winHeight
import pygame
from time import time

class InventoryOverlay(Overlay):
    def __init__(self, game):
        super().__init__(game)
        self.width = winWidth
        self.height = winHeight
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.lastInventoryPollTime = 0
        self.inventoryPollDelay = 10
        self.iitems = []
        self.itemComps = pygame.sprite.Group()
        self.loadComps()
        self.render()
    def loadComps(self):
        self.menuBg = pygame.Surface((800, 600), pygame.SRCALPHA).convert_alpha()
        self.menuBg.fill((15, 15, 15, 255))
        self.exitBtn = Button(
            self.game,
            (1020, 60),
            text = "X",
            groups = [self.comps],
            center = True,
            rounded = False,
            colors = ((20, 20, 20), (50, 50, 50)),
            textColors = ((100, 100, 100), (100, 100, 100)),
            wh = (20, 20)
        )
        self.itemsBtn = Button(
            self.game,
            (240, 60),
            center = True,
            text = "Items",
            groups = [self.comps],
            colors = ((20, 20, 20), (50, 50, 50)),
            textColors = ((100, 100, 100), (100, 100, 100)),
            wh = (80, 20),
            rounded = False
        )
    def pollInventory(self):
        """Poll the inventory for items"""
        self.iitems = self.game.player.inventory.items.items()
        print(self.iitems)
    def update(self):
        if self.active:
            if self.exitBtn.clicked:
                self.deactivate()
                self.game.closeInventory()
            if time() - self.lastInventoryPollTime >= self.inventoryPollDelay:
                self.pollInventory()
                self.lastInventoryPollTime = time()
            self.render()
            self.comps.update()
    def render(self):
        self.image.fill((0, 0, 0, 127))
        self.image.blit(self.menuBg, (self.width / 2 - 400, self.height / 2 - 300))
        for comp in self.comps:
            self.image.blit(comp.image, comp.rect)
        for itemComp in self.itemComps:
            self.image.blit(itemComp.image, itemComp.rect)