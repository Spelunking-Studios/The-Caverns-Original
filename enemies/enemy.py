import math
import random

import fx
import pygame
from animations import *
from objects import *
from player import *
from stgs import *

print('yo')
class Enemy(pygame.sprite.Sprite):
    pos = pygame.Vector2((0, 0))
    moveType = 1
    health = 5
    damage = 5
    points = 5
    color = False
    imgSheet = {'tileWidth': 32 ,'r': pygame.surface.Surface((32,32))}
    vel = 5
    startDir = (0, 0)
    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.enemies, game.layer2
        self.lID = objT.id
        self.game = game
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.loadAnimations()
        self.width = self.imgSheet['tileWidth']
        self.height = self.imgSheet['tileWidth']
        
        self.pos = pygame.Vector2((objT.x, objT.y))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.imgSheet['tileWidth'], self.imgSheet['tileWidth'])
        self.dir = pygame.Vector2(self.startDir)
        
    
    def loadAnimations(self):
        self.animations = animation2(self)

    def update(self):
        self.move()

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        if self.health <= 0:
            self.kill()
        
        self.animations.update()

    ## Vertical or horizontal movement
    def move(self):
        testVec = pygame.Vector2((self.pos.x, self.pos.y))
        if self.collideCheck(testVec + (self.dir*self.vel)):
            if not self.dir.x == 0:
                self.dir = pygame.Vector2((-self.dir.x, 0))
            elif not self.dir.y == 0:
                self.dir = pygame.Vector2((0, -self.dir.y))

        self.pos += self.dir *self.vel 
        

    def collideCheck(self, vector):
        returnVal = False
    
        testRect = pygame.Rect(round(vector.x), round(vector.y), self.rect.width, self.rect.height)
        for obj in self.game.colliders:
            if testRect.colliderect(obj.rect):
                returnVal = True
            
        return returnVal
    
    def deathSound(self):
        pass
    
    def takeDamage(self, damage):
        if pygame.time.get_ticks() - self.lastHit >= 200:
            self.health -= damage
            self.animations.lastHit = pygame.time.get_ticks()
            self.lastHit = pygame.time.get_ticks()
