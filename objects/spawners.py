import pygame
from animations import *
from stgs import *
import enemies
import util

class Spawner(util.Sprite):
    '''
    The base class for an entity spawner that repeatedly spawns entites based on a rectangular area 
    '''
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        # Defaults
        self.mob = None # Type of entity spawned
        self.rate = 5000 # Rate in milliseconds

        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v
        
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

        self.lastSpawn = now() # Tracks the last moment an enemy was summoned


    def update(self):
        if now()-self.lastSpawn >= self.rate:
            self.spawn()
    
    def spawn(self):
        pass

def Spawner1(game, objT):
    return Spawner(game, objT, mob=enemies.zombie)
