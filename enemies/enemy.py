import math
import random

import fx
import pygame
from animations import *
from objects import *
from player import *
from stgs import *

# Base Enemy class - should be inherited by all enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.groups.enemies, game.layer2
        self.health = 5
        self.damage = 5
        self.points = 1
        self.speed = 1
        self.lID = objT.id
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.game = game
        self.active = False
        self.detectionRange = 120
        self.pos = pygame.Vector2(objT.x, objT.y)
        self.rect = pygame.Rect(objT.x, objT.x, 64, 64)
        self.lastAttack = now()
        self.attackDelay = 60
        self.width, self.height = 64, 64
        self.lastHit = 0
        self.image = pygame.Surface((self.width, self.height))
        self.origImage = self.image.copy()
        self.animations = Animation(self)
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)
    def update(self):
        if self.health <= 0:
            self.kill()
        self.checkForActivation()
    def move(self):
        """Move the enemy"""
        testVec = pygame.Vector2(self.pos)
        testVec.x += self.vel.x * self.speed
        if not self.collideCheck(testVec):
            self.pos.x += self.vel.x * self.speed
        testVec = pygame.Vector2(self.pos)
        testVec.y += self.vel.y * self.speed
        if not self.collideCheck(testVec):
            self.pos.y += self.vel.y * self.speed
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
                if now() - self.lastAttack >= self.attackDelay:
                    self.game.player.takeDamage(self.damage)
        self.image = pygame.transform.rotate(self.origImage, self.angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)
    def collideCheck(self, vector):
        testRect = pygame.Rect(0, 0, 32, 32)
        testRect.center = vector
        for obj in self.game.groups.colliders:
            if testRect.colliderect(obj.rect) and not obj == self:
                return True
        
        return False
    def takeDamage(self, damage):
        self.health -= damage
        self.animations.fx(HurtFx())
        self.game.mixer.playFx('hit1')
        self.lastHit = pygame.time.get_ticks()
    def deathSound(self):
        pass
    def checkForActivation(self):
        """Check to see if the enemy should activate"""
        if self.active:
            return
        playerPos = pygame.Vector2(self.game.player.rect.center)
        mePos = self.rect
        playerPos.x -= mePos.centerx
        playerPos.y -= mePos.centery
        if playerPos.length() < self.detectionRange:
            self.activate()
    def activate(self):
        """Activate the enemy"""
        self.active = True