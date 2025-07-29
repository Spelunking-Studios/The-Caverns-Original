import random

from src import fx
from src import util
import pygame
from src.animations import *
from src.stgs import *
   
class Door(util.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites
        super().__init__(self.groups)
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.game = game
        self.targetRoom = 'room1-floor1'
        self.targetObj = "entrance"

        self.dump(kwargs, objT.properties) 
    
    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.pause = True
            def func():
                self.game.unPause()
                self.game.map.switchRoom(self.targetRoom, self.targetObj)
                fx.FadeIn(self.game)
            fx.FadeOut(self.game, onEnd=func)

class Entrance(util.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

        self.dump(kwargs, objT.properties) 

def Entrance1(game, objT):
    return Entrance(game, objT)

def Entrance2(game, objT):
    return Entrance(game, objT)

def Entrance3(game, objT):
    return Entrance(game, objT)

def Entrance4(game, objT):
    return Entrance(game, objT)

class Teleporter(util.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.level = self.game.map.getRoom()
        self.lID = objT.id
        self.target = 0
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        self.dest = self.level.getObjById(self.target)
        self.targetPos = pygame.Vector2(self.dest.x, self.dest.y)

    def update(self):
        if self.game.player.moveRect.colliderect(self.rect):
            self.game.pause = True
            def func():
                self.game.unPause()
                self.game.player.setPos((self.targetPos.x, self.targetPos.y), True)
                fx.FadeIn(self.game)

            fx.FadeOut(self.game, onEnd=func)
        #self.image = pygame.Surface((self.rect.width, self.rect.height))
        #self.image.fill(self.color)

class Exit(util.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.game = game

        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v
    
    def update(self):
        if self.rect.colliderect(self.game.player.moveRect):
            self.game.pause = True
            def func():
                self.game.unPause()
                self.game.map.nextFloor()
            fx.FadeOut(self.game, onEnd=func)
