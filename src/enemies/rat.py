import pygame
from .enemy import Enemy
from stgs import *
import animations
import math, random

ratImage = None

class Rat(Enemy):
    """A rat enemy"""
    def __init__(self, game, objT):
        global ratImage
        super().__init__(game, objT)

        self.health = 20
        self.damage = 2
        self.width = 48
        self.height = 48
        self.angle = 0
        self.speed = 190
        self.attackDelay = 620
        self.rand = random.randrange(0, 360, 45)
        
        if not ratImage:
            ratImage = pygame.image.load(asset("enemies", "rat", "rat2.png")).convert_alpha()
        
        self.image = ratImage#pygame.transform.scale(ratImage, (self.width, self.height))
        self.origImage = self.image.copy()
        self.rect = pygame.Rect(objT.x, objT.y, self.width, self.height)
    def move(self):
        """Move the rat"""
        testVec = pygame.Vector2(self.pos)
        testVec.x += self.vel.x * (self.speed * self.game.dt())
        if not self.collideCheck(testVec):
            self.pos.x += self.vel.x * (self.speed * self.game.dt())
        testVec = pygame.Vector2(self.pos)
        testVec.y += self.vel.y * (self.speed * self.game.dt())
        if not self.collideCheck(testVec):
            self.pos.y += self.vel.y * (self.speed * self.game.dt())
        self.setAngle()
        wobble = math.sin(pygame.time.get_ticks()/100+self.rand)*20
        self.angle -= wobble
        self.rotateImage()
        self.vel.rotate_ip(wobble)
        self.rect.center = self.pos
    def update(self):
        super().update()
        # Move towards the player
        self.move()
        self.animations.update()
    def kill(self):
        super().kill()
