import pygame
from src.stgs import *
from src import util
import random
# from src.enemies import Beetle, SilverBeetle, FireBeetle, RockCreature, BoomBug, Bat, DemonBat
import src.enemies as enemies
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
        self.include_bat = True
        self.include_demon_bat = False
        self.include_silver = False
        self.include_red = False
        self.include_boom = False
        self.include_rock = False

        self.max_silver = 5 # Silver Beetles destroy FPS

        self.dump(kwargs, objT.properties) 

        if self.include_standard:
            self.creatures.append(enemies.Beetle)
        if self.include_bat:
            self.creatures.append(enemies.Bat)
        if self.include_demon_bat:
            self.creatures.append(enemies.DemonBat)
        if self.include_silver:
            self.creatures.append(enemies.SilverBeetle)
        if self.include_red:
            self.creatures.append(enemies.FireBeetle)
        if self.include_boom:
            self.creatures.append(enemies.BoomBug)

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
        total_silver = 0
        while total > 0:
            creature = random.choice(self.creatures) 
            if creature == enemies.SilverBeetle:
                total_silver += 1
                if total_silver == self.max_silver:
                    self.creatures.remove(enemies.SilverBeetle)
            x, y = get_random_zone_position(self.game)
            c = creature(self.game, util.ObjT(x=x, y=y))
            c.start()
            total -= creature.challenge_rating
