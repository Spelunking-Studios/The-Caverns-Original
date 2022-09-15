from .overlay import Overlay
from menu import Button, Image
import colors
from stgs import winWidth, winHeight, asset
import pygame
from time import time

cachedImages = {}

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
        self.lastOpenTime = 0
        self.openDelay = 1
        self.itemComps = pygame.sprite.Group()
        self.loadComps()
        self.render()
    def loadComps(self):
        """Loads all of the components"""
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
        for item in self.itemComps:
            item.kill()
        i = 0
        for item in self.iitems:
            if not item[0] in cachedImages:
                cachedImages[item[0]] = pygame.transform.scale(
                    pygame.image.load(
                        asset("items", item[1]["category"], item[0] + ".png")
                    ),
                    (32, 32)
                )
            offset = list(self.getOffset())
            offset[0] += 10 + ((32 * i) % 50)
            offset[1] += 30 + ((32 * i) % 50)
            p = (offset[0], offset[1])
            Image(cachedImages[item[0]], p, groups = [self.itemComps])
            i += 1
        print("Polled inventory.")
    def update(self):
        """Update (DUH)"""
        if self.active:
            if self.exitBtn.clicked:
                self.deactivate()
                self.game.closeInventory()
            if time() - self.lastInventoryPollTime >= self.inventoryPollDelay:
                self.pollInventory()
                self.lastInventoryPollTime = time()
            self.comps.update()
            self.render()
    def activate(self):
        """Activate the inventory"""
        if time() - self.lastOpenTime >= self.openDelay:
            self.lastOpenTime = time()
            super().activate()
            self.game.inInventory = True
    def deactivate(self):
        """Deactivate the inventory"""
        super().deactivate()
        self.game.inInventory = False
    def render(self):
        """Render the inventory"""
        self.image.fill((0, 0, 0, 127))
        self.image.blit(self.menuBg, self.getOffset())
        for comp in self.comps:
            self.image.blit(comp.image, comp.rect)
        for itemComp in self.itemComps:
            self.image.blit(itemComp.image, itemComp.rect)
    def getOffset(self):
        return (self.width / 2 - 400, self.height / 2 - 300)