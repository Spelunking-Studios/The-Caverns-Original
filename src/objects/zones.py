from src import util
import pygame
import random
from src.stgs import *
import src.enemies

class Zone(util.Sprite):
    '''
    The base class for an entity spawner that repeatedly spawns entites based on a rectangular area 
    '''
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.groups.zones
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.dump(kwargs, objT.properties) 
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

    def spawn(self, entity):
        e = entity()
        e.position = self.random_position()


    def random_position(self):
        return (random.uniform(self.rect.left, self.rect.right), random.uniform(self.rect.top, self.rect.bottom))
    
    # def draw(self, surf, transform):
    #     pygame.draw.rect(surf, (200, 0, 0), transform(self.rect), 6)
    #     pygame.draw.circle(surf, util.white, self.game.cam.applyTuple(self.random_position()), 4)
