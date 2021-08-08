import random

import fx
import pygame
from animations import *
from objects import *
from player import *
from stgs import *

from . import enemy

class enemyBullet(pygame.sprite.Sprite):
    pos = pygame.Vector2((0,0))
    image = pygame.image.load(asset('objects/bullet2.png'))
    vel = 4
    offset = 0
    damage = 5
    friendly = False
    def __init__(self, game, pos, target, angle, **kwargs):
        self.groups = game.sprites, game.eBullets, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(target).normalize()
        self.dir = self.dir.rotate(self.offset)
        self.image = pygame.transform.rotate(self.image, angle - self.offset)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = self.pos
    
    def update(self):
        self.move()  
    
    def move(self):
        self.pos += self.dir *self.vel
        self.rect.center = self.pos