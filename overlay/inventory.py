from .overlay import Overlay
from menu import Button
import colors
from stgs import winWidth, winHeight
import pygame

class InventoryOverlay(Overlay):
    def __init__(self, game):
        super().__init__(game)
        self.width = winWidth
        self.height = winHeight
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
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
    def update(self):
        if self.active:
            if self.exitBtn.clicked:
                self.deactivate()
                self.game.closeInventory()
            self.render()
            self.comps.update()
    def render(self):
        self.image.fill((0, 0, 0, 127))
        self.image.blit(self.menuBg, (self.width / 2 - 400, self.height / 2 - 300))
        for comp in self.comps:
            self.image.blit(comp.image, comp.rect)