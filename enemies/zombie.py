import math
import random

import fx
import pygame
from animations import *
from objects import *
from player import *
from stgs import *

from . import enemy
from .eBullet import EnemyBullet

class Zombie(enemy.Enemy):

    def __init__(self, game, objT):
        super().__init__(game, objT, )#groups = [game.sprites, game.enemies, game.layer2, game.colliders])

        self.pos = pygame.Vector2(objT.x, objT.y)
        self.vel = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.speed = 2*deltaConst
        self.health = 15
        self.lastShoot = now()
        self.lastAttack = now()
        self.attackDelay = 360
        self.shootRate = random.randrange(2500, 5000, 50)
        self.animations = RotAnimation(self, asset('enemies/zombie1.png'))
        self.animations.delay = 60
        self.angle = 0
    
    def move(self):
        testVec = pygame.Vector2(self.pos)
        testVec.x += self.vel.x *self.speed
        if not self.collideCheck(testVec):
            self.pos.x += self.vel.x *self.speed 

        testVec = pygame.Vector2(self.pos)
        testVec.y += self.vel.y *self.speed
        if not self.collideCheck(testVec):
            self.pos.y += self.vel.y *self.speed 

        self.setAngle()
        
        self.rect.center = self.pos

    def setAngle(self):
        mPos = pygame.Vector2(self.game.player.rect.center)
        pPos = self.rect
        mPos.x -= pPos.centerx 
        mPos.y -= pPos.centery
        if mPos.length() > 500:
            self.vel = pygame.Vector2(0, 0)
            self.animations.freeze = True

        else:
            self.animations.freeze = False
            if mPos.length() > 20: 
                try:
                    mPos.normalize_ip()
                    self.angle = math.degrees(math.atan2(-mPos.y, mPos.x)) #+ random.randrange(-2, 2)
                    self.vel = mPos
                except ValueError:
                    self.angle = 0
                    self.vel = pygame.Vector2(0, 0)
                self.angle -= 90
            else:
                self.vel = pygame.Vector2(0, 0)
                if now()-self.lastAttack >= self.attackDelay:
                    self.game.player.takeDamage(5)
        
    def collideCheck(self, vector):
        testRect = pygame.Rect(0, 0, 32, 32)
        testRect.center = vector
        for obj in self.game.colliders:
            if testRect.colliderect(obj.rect) and not obj == self:
                return True
        
        return False

    def rotCenter(self, angle=False):
        if not angle:
            angle = self.angle
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)

    def takeDamage(self, damage):
        self.health -= damage
        self.animations.fx(HurtFx())
        self.game.mixer.playFx('hit1')
        self.lastHit = pygame.time.get_ticks()

    # def deathSound(self):
    #     self.game.mixer.playFx('hit2')
        
    def kill(self):
        #fx.particles(self.game, self.rect, lifeSpan = 400, tickSpeed=2, size = 14).setParticleKwargs(speed=1.5, shrink=0.4, life=140, color=colors.red)
        super().kill()
    
    def update(self):
        super().update()
        self.animations.update()
        
