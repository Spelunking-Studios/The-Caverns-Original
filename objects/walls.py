import random

import fx
import pygame
from animations import *
from stgs import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.groups = game.groups.colliders, game.layer1 if DEBUG else game.groups.colliders
        super().__init__(self.groups)
        self.objT = objT
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.color = (255, 255, 255)
        self.targetObj = "Entrance"
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        if DEBUG:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(self.color)
