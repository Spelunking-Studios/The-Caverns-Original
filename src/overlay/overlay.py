from src import util
import pygame


class Overlay(util.Sprite):
    def __init__(self, game):
        super().__init__(game.overlayer)
        self.game = game
        self.width = 200
        self.height = 200
        self.image = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        ).convert_alpha()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.comps = pygame.sprite.Group()
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def update(self):
        if self.active:
            self.render()

    def render(self):
        self.image.fill((0, 0, 0, 190))
