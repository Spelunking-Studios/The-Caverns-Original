import random

import fx
import pygame
from animations import *
from stgs import *


class key(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, image, **kwargs):
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        game.level.key = self

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.image.load(image)
        self.pos = pygame.Vector2(objT.x, objT.y)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

class key1(key):
    def __init__(self, game, objT):
        super().__init__(game, objT, asset('objects/decryptor.png'))
