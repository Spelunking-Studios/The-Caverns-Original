import pygame
from stgs import *
import util
import random
from src.enemies import Beetle, SilverBeetle
from src.scripts import get_random_zone_position

class Nest(util.Sprite):
    '''
    '''

    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.groups.zones
        pygame.sprite.Sprite.__init__(self, self.groups)
        

        self.creatures = []
        self.challenge_rating = 10
        self.include_standard = True
        self.include_silver = False

        self.dump(kwargs, objT.properties) 

        if self.include_standard:
            self.creatures.append(Beetle)
        if self.include_silver:
            self.creatures.append(SilverBeetle)

        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.loaded = False

    def update(self):
        if not self.loaded:
            self.spawn()
            self.loaded = True
    #     if now()-self.lastSpawn >= self.rate:
    #         self.spawn()
    
    def spawn(self):
        total = self.challenge_rating
        while total > 0:
            creature = random.choice(self.creatures) 
            x, y = get_random_zone_position(self.game)
            c = creature(self.game, util.ObjT(x=x, y=y))
            c.start()
            total -= creature.challenge_rating



