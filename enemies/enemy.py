import math
import random

import fx
import pygame
from animations import *
from objects import *
from player import *
from stgs import *
from effects import HurtEffect

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
        self.reach = 20
        self.game = game
        self.active = False
        self.detectionRange = 200
        self.pos = pygame.Vector2(objT.x, objT.y)
        self.rect = pygame.Rect(objT.x, objT.x, 64, 64)
        self.rect.center = (objT.x, objT.y)
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
        self.attemptToDealDamage()
    def move(self):
        """Move the enemy"""
        testVec = pygame.Vector2(self.pos)
        testVec.x += self.vel.x * self.speed * self.game.dt()
        if not self.collideCheck(testVec):
            self.pos.x += self.vel.x * self.speed * self.game.dt()
        testVec = pygame.Vector2(self.pos)
        testVec.y += self.vel.y * self.speed * self.game.dt()
        if not self.collideCheck(testVec):
            self.pos.y += self.vel.y * self.speed * self.game.dt()
        self.setAngle()
        self.rect.center = self.pos
    def setAngleFacingTarget(self, targetPos):
        """Rotates the bat to face the target position"""
        mPos = targetPos
        pPos = self.rect
        mPos.x -= pPos.centerx
        mPos.y -= pPos.centery

<<<<<<< HEAD
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
                    self.lastAttack = now()
=======
        try:
            mPos.normalize_ip()
            self.angle = math.degrees(math.atan2(-mPos.y, mPos.x)) #+ random.randrange(-2, 2)
            self.vel = mPos
        except ValueError:
            self.angle = 0
            self.vel = pygame.Vector2(0, 0)
        self.angle -= 90
        self.rotateImage()
    def rotateImage(self):
>>>>>>> 59365beabc2204ad7a6daacc018bb488a7b1dba3
        self.image = pygame.transform.rotate(self.origImage, self.angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)
    def setAngle(self):
        self.setAngleFacingTarget(pygame.Vector2(self.game.player.rect.center))
    def collideCheck(self, vector):
        testRect = pygame.Rect(0, 0, 32, 32)
        testRect.center = vector
        for obj in self.game.groups.colliders:
            if testRect.colliderect(obj.rect) and not obj == self:
                return True
        
        return False
    def takeDamage(self, damage):
        self.health -= damage
        self.animations.fx(HurtEffect())
        self.game.mixer.playFx('hit1')
        self.lastHit = pygame.time.get_ticks()
    def attemptToDealDamage(self):
        """Attempt to deal damage to the player"""
        mPos = pygame.Vector2(self.game.player.rect.center)
        pPos = self.rect
        mPos.x -= pPos.centerx
        mPos.y -= pPos.centery
        if mPos.length() < self.reach and (True or now() >= self.attackDelay + self.lastAttack):
            self.lastAttack = now()
            self.game.player.takeDamage(self.damage)
            #self.pickEndPos(self.angle, pickRandom = True)
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
    def vecsAreSemiEqual(self, vec1, vec2, error = 10):
        """Checks if the vectors are within error (10) of eachother"""
        # Make sure the vectors exist
        if not vec1 or not vec2:
            return False
        # Make 2 rects
        rect1 = pygame.Rect(vec1.x, vec1.y, error, error)
        rect2 = pygame.Rect(vec2.x, vec2.y, error, error)
        # Check for collision/overlap
        return rect1.colliderect(rect2)
    def vecsAreEqual(self, vec1, vec2):
        if not vec1 or not vec2:
            return False
        if int(vec1.x) == int(vec2.x) and int(vec1.y) == int(vec2.y):
            return True
        return False