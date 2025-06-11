import math
import random
from time import time
import fx
import pygame
import util
from animations import *
from objects import *
from player import *
from stgs import *
from effects import HurtEffect

class SimpleEnemy(util.Sprite):
    """Base enemy class"""
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.groups.enemies, game.layer2
        self.objT = objT
        self.lID = objT.id
        self.pos = pygame.Vector2(objT.x, objT.y)

        self.last_hit = 0
        
        self.health = 40

        self.dump(kwargs, objT.properties)
        super().__init__(self.groups)

    def take_damage(self, dmg):
        self.last_hit = now()
        self.health -= dmg
        self.game.mixer.playFx('hit1')

    def update(self):
        if self.health <= 0:
            self.kill()

    def take_knockback(self, other):
        pass

    def kill(self):
        super().kill()
        # Will eventually implement a blood splatter effect when killing enemies
        # self.game.blood_splatter()
