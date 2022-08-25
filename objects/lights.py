import random

import fx
import pygame
from animations import *
from stgs import *


class LightSource(pygame.sprite.Sprite):
    img = asset('objects/light2.png')
    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.groups.lightSources
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.pos = pygame.Vector2((self.rect.x, self.rect.y))
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.sourceImg = pygame.image.load(self.img).convert_alpha()
        self.rect = self.sourceImg.get_rect(center=self.rect.center)

        if not isinstance(objT, pygame.Rect):
            for k, v in objT.properties.items():
                self.__dict__[k] = v

class LightEffect(LightSource):
    def __init__(self, game, rect, **kwargs):
        self.life = 200
        self.init = now()
        super().__init__(game, rect, img=asset("objects/light1.png"))
    
    def update(self):
        if now()-self.init >= self.life:
            self.kill()


