import random

import fx
import pygame
from animations import *
from stgs import *

class consumable(pygame.sprite.Sprite):
    imgSheet = {'active': False, 'static': True,'tileWidth': 32}
    image = pygame.Surface((imgSheet['tileWidth'], imgSheet['tileWidth']))

    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.items, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        if self.imgSheet['active']:
            self.animations = animation(self)

        self.pos = pygame.Vector2(objT.x, objT.y)
        self.rect = pygame.Rect(0, 0, self.imgSheet['tileWidth'], self.imgSheet['tileWidth'])
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self):
        if self.imgSheet['active']:
            self.animations.update()
  