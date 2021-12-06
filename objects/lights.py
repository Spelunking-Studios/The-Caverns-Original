import random

import fx
import pygame
from animations import *
from stgs import *


class LightSource(pygame.sprite.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.groups.lightSources
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.pos = pygame.Vector2((self.rect.x, self.rect.y))
        self.sourceImg = pygame.image.load(asset('objects/light2.png')).convert_alpha()
        self.rect = self.sourceImg.get_rect(center=self.rect.center)
        for k, v in kwargs.items():
            self.__dict__[k] = v

        for k, v in objT.properties.items():
            self.__dict__[k] = v
