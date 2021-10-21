import math
import random

import fx
import pygame
from animations import *
from objects import *
from player import *
from stgs import *

# Base Enemy class - should be inherited by all enemies
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.enemies, game.layer2
        self.health = 5
        self.damage = 5
        self.points = 5
        self.lID = objT.id
        self.game = game
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.w, h = 64, 64
        self.lastHit = 0 
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        if self.health <= 0:
            self.kill()
        self.move()

    ## Vertical or horizontal movement
    def move(self):
        pass
        # testVec = pygame.Vector2((self.pos.x, self.pos.y))
        # if self.collideCheck(testVec + (self.dir*self.vel)):
        #     if not self.dir.x == 0:
        #         self.dir = pygame.Vector2((-self.dir.x, 0))
        #     elif not self.dir.y == 0:
        #         self.dir = pygame.Vector2((0, -self.dir.y))

        # self.pos += self.dir *self.vel 
        

    def collideCheck(self, vector):
        testRect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        testRect.center = vector
        for obj in self.game.colliders:
            if testRect.colliderect(obj.rect):
                return True
        
        return False
    
    def takeDamage(self, damage):
        self.health -= damage
        self.animations.fx(HurtFx())
        self.game.mixer.playFx('hit1')
        self.lastHit = pygame.time.get_ticks()

    def deathSound(self):
        pass
    
