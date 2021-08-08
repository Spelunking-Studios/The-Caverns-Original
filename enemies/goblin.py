import math
import random

import fx
import pygame
from animations import *
from objects import *
from player import *
from stgs import *

from . import enemy
from .eBullet import enemyBullet

class goblin(enemy.Enemy):

    def __init__(self, game, objT):
        imgSheet = {'tileWidth': 64, 
            'r': asset('enemies/goblinR.png'), 
            'l': asset('enemies/goblinL.png'), 
            'd': asset('enemies/goblinD.png'), 
            'u': asset('enemies/goblinU.png')}
        self.vertical = False
        self.evil = False

        super().__init__(game, objT, health = 2, imgSheet = imgSheet)
        if self.vertical:
            self.dir = pygame.Vector2(0, random.randrange(-1, 1+1, 2))
        else:
            self.dir = pygame.Vector2(random.randrange(-1, 1+1, 2), 0)
        self.spawnLoc = pygame.Vector2(objT.x, objT.y)
        self.moveRadius = 100
        self.vel = 3
        self.health = 20
        self.lastHit = 0
        self.lastShoot = pygame.time.get_ticks()
        self.shootRate = random.randrange(2500, 5000, 50)
    
    
    def move(self):
        testVec = pygame.Vector2((self.pos.x, self.pos.y))
        if self.collideCheck(testVec + (self.dir*self.vel)) or self.spawnLoc.distance_to(testVec + (self.dir*self.vel)) >= self.moveRadius:
            if not self.dir.x == 0:
                self.dir = pygame.Vector2((-self.dir.x, 0))
            else:
                self.dir = pygame.Vector2((0, -self.dir.y))

        self.pos += self.dir *self.vel 
    
    def takeDamage(self, damage):
        if pygame.time.get_ticks() - self.lastHit >= 200:
            self.health -= damage
            self.animations.fx(hurtFx())
            self.lastHit = pygame.time.get_ticks()

    def deathSound(self):
        self.game.mixer.playFx('hit2')
        
    def kill(self):
        fx.particles(self.game, self.rect, lifeSpan = 400, tickSpeed=2, size = 14).setParticleKwargs(speed=1.5, shrink=0.4, life=140, color=colors.red)
        super().kill()
    
    def update(self):
        super().update()
        if self.evil:
            if pygame.time.get_ticks() -self.lastShoot >= self.shootRate:
                angVec = pygame.Vector2(self.game.player.rect.x-self.rect.x, self.game.player.rect.y-self.rect.y)
                enemyBullet(self.game, self.rect.center, angVec, math.degrees(math.atan2(-angVec.normalize().y, angVec.normalize().x))),
                self.lastShoot = pygame.time.get_ticks()
                self.shootRate = random.randrange(2500, 5000, 50)
                self.game.mixer.playFx('launch1')
