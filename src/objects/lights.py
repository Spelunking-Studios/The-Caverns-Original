import util
import random

import fx
import pygame
from animations import *
from stgs import *


class LightSource(util.Sprite):
    sourceImg = pygame.image.load(asset("objects/light2.png"))

    # objT may also be a Rect()

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.groups.lightSources
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.pos = pygame.Vector2((self.rect.x, self.rect.y))
        for k, v in kwargs.items():
            self.__dict__[k] = v

        if not isinstance(objT, pygame.Rect):
            for k, v in objT.properties.items():
                self.__dict__[k] = v
        
        self.image = self.sourceImg.copy().convert_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)

    def resize_scale(self, new_scale):
        w, h = self.rect.size
        self.image = pygame.transform.scale(self.sourceImg, (int(w*new_scale), int(h*new_scale)))

    def resize_wh(self, w, h):
        self.image = pygame.transform.scale(self.sourceImg, (int(w), int(h)))

class LightEffect(LightSource):
    def __init__(self, game, rect, **kwargs):
        self.life = 900
        self.scale = 1
        self.init = now()
        super().__init__(game, rect, img=asset("objects/light1.png"), **kwargs)
    
        # if self.scale != 1:
        #     self.resize(new_scale)
        self.resize_wh(rect.w, rect.h)

    def update(self):
        if now()-self.init >= self.life:
            self.kill()


