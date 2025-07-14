import math
import random
from time import time
from src import fx
import pygame
from src import util
from src.animations import *
from src.objects import *
from src.player import *
from src.stgs import *
from src.effects import HurtEffect

class SimpleEnemy(util.Sprite):
    """Base enemy class"""
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.groups.enemies, game.layer2
        self.objT = objT
        self.lID = objT.id
        self.pos = pygame.Vector2(objT.x, objT.y)
        self.particles = None

        self.last_hit = 0
        
        self.health = 40

        self.dump(kwargs, objT.properties)
        super().__init__(self.groups)

    def take_damage(self, dmg):
        self.last_hit = now()
        self.health -= dmg
        self.game.mixer.playFx('hit1')

    def deal_damage(self, dmg=4):
        self.game.player.take_damage(dmg)

    def update(self):
        if self.health <= 0:
            self.kill()

    def take_knockback(self, other):
        pass

    def splat(self, pos=None):
        if not pos:
            pos = self.rect.center

        self.game.map.floor.room.blit(img, pos)

    def kill(self):
        if hasattr(self, "challenge_rating"):
            self.game.points += 10*self.challenge_rating
        else:
            self.game.points += 5
        super().kill()
        # Will eventually implement a blood splatter effect when killing enemies
        # sef.game.blood_splatter()
