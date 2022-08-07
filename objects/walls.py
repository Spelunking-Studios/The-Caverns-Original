import random

import fx
import pygame
from animations import *
from stgs import *


class Wall(pygame.sprite.Sprite):
    

    def __init__(self, room, objT, **kwargs):
        #self.groups = game.groups.colliders, game.layer1 if DEBUG else game.groups.colliders
        pygame.sprite.Sprite.__init__(self)
        self.room = room
        self.objT = objT
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.color = (255, 255, 255)
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

class PlatformWall(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, objT, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.objT = objT
        
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v
            
        self.image = pygame.Surface((self.rect.width, self.rect.height))