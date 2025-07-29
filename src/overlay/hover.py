from src import util
import pygame
from src.stgs import winWidth, winHeight, asset, checkKey, fonts


class HoverOverlay(util.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.overlayer)
        self.components = pygame.sprite.Group()
        self.text = None
        self.render = None
        self.active = True
        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.color = util.white

    def deactivate(self):
        self.active = False

    def update(self):
        self.text = None
        enemies = self.game.groups.getProximitySprites(
                self.game.player,
                800,
                groups=[self.game.groups.enemies]
            )
        for e in enemies:
            mouse_rect = pygame.Rect(self.game.get_mouse_pos()[0], self.game.get_mouse_pos()[1], 1, 1)
            if mouse_rect.colliderect(self.game.cam.applyRect(e.rect)):
                self.text = e

    def draw(self, ctx, transform=None):
        transform = transform if transform else self.game.cam.applyRect
        if self.text:
            if not self.render:
                if hasattr(self.text, "name"):
                    text = self.text.name
                else:
                    text = self.text.__class__.__name__
                self.render = fonts['hover'].render(
                    text,
                    self.game.antialiasing,
                    self.color
                )
            ctx.blit(self.render, transform(self.text.rect).midtop)
        else:
            self.render = None

