import random

import fx
import pygame
from animations import *
from stgs import *
   
class Door(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.game = game
        self.targetLevel = 'cave1'
        self.targetId = "entrance"
        #self.game.level.door = self
        #self.image = pygame.Surface((objT.width, objT.height))
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        #self.parts = fx.particles(self.game, pygame.Rect(self.rect.x, self.rect.y, 64, 12), tickSpeed=2, size = 14)
        #self.parts.setParticleKwargs(speed=1.5, shrink=0.4, life=140, color=colors.orangeRed)
    
    def update(self):
        if self.rect.colliderect(self.game.player.moveRect):
            self.game.pause = True
            def func():
                self.game.unPause()
                self.game.map.switchLevel(self.targetLevel, self.targetId)
            fx.FadeOut(self.game, onEnd=func)

class Entrance(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.lID = objT.id
        #game.level.entrance = self
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        #self.image = pygame.Surface((self.rect.width, self.rect.height))
        #self.image.fill(self.color)

def Entrance1(game, objT):
    return Entrance(game, objT)

def Entrance2(game, objT):
    return Entrance(game, objT)

def Entrance3(game, objT):
    return Entrance(game, objT)

def Entrance4(game, objT):
    return Entrance(game, objT)

class Teleporter(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.level = self.game.map.level
        self.lID = objT.id
        self.target = 0
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        for obj in self.level.tmxdata.objects:
            if obj.id == self.target:
                self.targetPos = pygame.Vector2(obj.x*self.level.scale, obj.y*self.level.scale)

    def update(self):
        if self.game.player.moveRect.colliderect(self.rect):
            self.game.pause = True
            def func():
                self.game.unPause()
                self.game.player.setPos((self.targetPos.x, self.targetPos.y), True)

            fx.FadeOut(self.game, onEnd=func)
        #self.image = pygame.Surface((self.rect.width, self.rect.height))
        #self.image.fill(self.color)