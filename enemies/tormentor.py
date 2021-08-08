import random
# Not all of these are required but are handy
import fx
import pygame
from animations import *
from objects import *
from player import *
from stgs import *

from . import enemy

class tormentor(enemy.Enemy):

    def __init__(self, game, objT):
        imgSheet = {'tileWidth': 64, 'r': asset('enemies/tormentor3.png'), 'l': asset('enemies/tormentor4.png'), 'd': asset('enemies/tormentor1.png'), 'u': asset('enemies/tormentor2.png')}
        self.vertical = False
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        if self.vertical:
            startDir = (0, random.randrange(-1, 1+1, 2))
        else:
            startDir = (random.randrange(-1, 1+1, 2), 0)
        super().__init__(game, objT, health = 2, imgSheet = imgSheet, startDir = startDir)
        self.spawnLoc = pygame.Vector2(objT.x, objT.y)
        self.moveRadius = 100
        self.vel = 3
    
    def collideCheck(self, vector):
        returnVal = False
    
        testRect = pygame.Rect(round(vector.x), round(vector.y), self.rect.width, self.rect.height)
        for obj in self.game.colliders:
            if not isinstance(obj, (mPlatform)):
                if testRect.colliderect(obj.rect):
                    returnVal = True
        
        return returnVal
    
    def move(self):
        testVec = pygame.Vector2((self.pos.x, self.pos.y))
        if self.collideCheck(testVec + (self.dir*self.vel)) or self.spawnLoc.distance_to(testVec + (self.dir*self.vel)) >= self.moveRadius:
            if not self.dir.x == 0:
                self.dir = pygame.Vector2((-self.dir.x, 0))
            else:
                self.dir = pygame.Vector2((0, -self.dir.y))

        self.pos += self.dir *self.vel 
    
    def kill(self):
        fx.particles(self.game, self.rect, lifeSpan = 400, tickSpeed=2, size = 14).setParticleKwargs(speed=1.5, shrink=0.4, life=140, color=colors.red)
        super().kill()
    
    def deathSound(self):
        self.game.mixer.playFx('hit1')