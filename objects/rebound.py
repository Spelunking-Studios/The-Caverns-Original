import random

import fx
import pygame
from animations import *
from stgs import *

class rebound(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.layer1, game.colliders
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.game = game
        self.points = 10
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        self.parts = fx.particles(self.game, pygame.Rect(self.rect.x, self.rect.y, 64, 12), tickSpeed=2, size = 14)
        self.parts.setParticleKwargs(speed=1.5, shrink=0.4, life=140, color=colors.lightGreen)

    def kill(self):
        self.parts.kill()
        super().kill()
