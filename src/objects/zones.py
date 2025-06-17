import util
import pygame
import random
from stgs import *
import enemies

class Zone(util.Sprite):
    '''
    The base class for an entity spawner that repeatedly spawns entites based on a rectangular area 
    '''
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.groups.zones
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v
        
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

    def spawn(self, entity):
        e = entity()
        e.position = self.random_position()


    def random_position(self):
        return (self.rect.x + self.rect.w*random.random(), self.rect.y + self.rect.h*random.random())
    
    # def draw(self, surf, transform):
    #     pygame.draw.rect(surf, (200, 0, 0), transform(self.rect), 6)
    #     pygame.draw.circle(surf, util.white, self.game.cam.applyTuple(self.random_position()), 4)
