from src import util
import pygame
from src.stgs import asset, checkKey


class MapOverlay(util.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.overlayer)
        self.components = pygame.sprite.Group()
        self.text = []
        self.active = False
        self.rect = pygame.Rect(0, 0, self.game.width(), self.game.height())
        self.image = pygame.Surface(
            (self.game.width(), self.game.height()),
            pygame.SRCALPHA
        )
        self.load_components()
        self.render()

    def load_components(self):
        for comp in self.components:
            comp.kill()

        self.mapImage = pygame.image.load(asset('gameMap.png'))
        self.mapImage = pygame.transform.scale(
            self.mapImage,
            (int(self.game.width()), int(self.game.height()))
        ).convert_alpha()

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def update(self):
        now = pygame.time.get_ticks()
        if self.active:
            self.render()
            self.components.update()
            if checkKey("map") and now - self.game.lastPause >= 180:
                self.deactivate()
                self.game.unPause()
                self.game.lastPause = now
        else:
            if checkKey("map") and now - self.game.lastPause >= 180:
                self.activate()
                self.game.pause = True
                self.game.lastPause = now

    def render(self):
        self.image.fill((0, 0, 0, 190))
        self.image.blit(self.mapImage, (0, 0))
