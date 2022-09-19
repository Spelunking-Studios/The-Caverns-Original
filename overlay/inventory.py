from .overlay import Overlay
from menu import Button, Image
import colors
from stgs import winWidth, winHeight, asset
import pygame, os
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
        self.lastChangeTime = 0
        self.changeDelay = 0.5
        self.itemComps = pygame.sprite.Group()
        self.loadComps()
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
        ix = 0
        iy = 0
        for item in self.iitems:
            print(item)
            if not item[0] in cachedImages:
                imagePath = asset("items", item[1]["category"], item[0] + ".png")
                if os.path.exists(imagePath):
                    cachedImages[item[0]] = pygame.transform.scale(pygame.image.load(imagePath).convert_alpha(), (64, 64))
                else:
                    cachedImages[item[0]] = pygame.transform.scale(pygame.Surface((1, 1), pygame.SRCALPHA).convert_alpha(), (64, 64))
            imref = cachedImages[item[0]]
            pos = (
                (self.width / 2 - 400) + 10 + (74 * (ix % 3)),
                (self.height / 2 - 300) + 30 + (74 * (iy % 3))
            )
            print(pos)
            i = Image(imref, self.game, pos, groups = [self.itemComps])
            print(i.rect)
            ix += 1
            if ix > 3:
                ix = 0
                iy += 1
        print(self.itemComps)
    def update(self):
        """Update (DUH)"""
        if self.active:
            if self.exitBtn.clicked:
                self.deactivate()
            if time() - self.lastInventoryPollTime >= self.inventoryPollDelay:
                self.pollInventory()
                self.lastInventoryPollTime = time()
            self.comps.update()
            self.itemComps.update()
            self.render()
    def checkIfActivationPossible(self):
        return time() - self.lastChangeTime >= self.changeDelay
    def activate(self):
        if self.checkIfActivationPossible():
            self.lastChangeTime = time()
            super().activate()
            if not self.game.inInventory:
                print("Warning: game's inventory overlay was not open. Opening it...")
                self.game.openInventory()
    def deactivate(self):
        """Deactivate the inventory"""
        super().deactivate()
        self.lastChangeTime = time()
        if self.game.inInventory:
            print("Warning: game's inventory overlay was not closed. Closing it...")
            self.game.closeInventory()
    def render(self):
        """Render the inventory"""
        self.image.fill((0, 0, 0, 127))
        self.image.blit(self.menuBg, self.getOffset())
        for comp in self.comps:
            self.image.blit(comp.image, comp.rect)
        for itemComp in self.itemComps:
            self.image.blit(itemComp.image, itemComp.rect)
    def getOffset(self):
        """Get the position of the upper left corner of the overlay
        
        Returns: tuple (x, y)
        """
        return (self.width / 2 - 400, self.height / 2 - 300)