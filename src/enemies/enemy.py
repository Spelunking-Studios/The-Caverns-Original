import math
import random
from time import time
import pygame
from src import util
from src.animations import *
from src.objects import *
from src.stgs import *
from src.effects import HurtEffect

class SimpleEnemy(util.Sprite):
    """Base enemy class"""
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.groups.enemies, game.layer2

        self.particles = None
        self.collision_type = 4

        self.last_hit = 0
        
        self.health = 40
        self.damage = 4

        if objT:
            self.objT = objT
            self.lID = objT.id
            self.pos = pygame.Vector2(objT.x, objT.y)
            self.dump(kwargs, objT.properties)
        else:
            self.dump(kwargs)
        super().__init__(self.groups)

    def take_damage(self, dmg):
        self.last_hit = now()
        self.health -= dmg
        self.game.mixer.playFx('hit1')

    def deal_damage(self):
        self.game.player.take_damage(self.damage)

    def update(self):
        if self.health <= 0:
            self.death()

    def take_knockback(self, other):
        pass

    def splat(self, pos=None):
        if not pos:
            pos = self.rect.center

        self.game.map.floor.room.blit(img, pos)

    def death(self):
        # to use instead of kill because changing levels kills enemies
        if hasattr(self, "challenge_rating"):
            self.game.points += 10*self.challenge_rating
        else:
            self.game.points += 5
        self.kill()

