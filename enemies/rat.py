import pygame
from .enemy import Enemy
from stgs import *
import animations

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
        self.speed = 90
        self.attackDelay = 620
        
        if not ratImage:
            ratImage = pygame.image.load(asset("enemies", "rat", "rat.png")).convert_alpha()
        
        self.image = pygame.transform.scale(ratImage, (self.width, self.height))
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
        self.rect.center = self.pos
    def update(self):
        super().update()
        # Move towards the player
        self.move()
        self.animations.update()
    def kill(self):
        super().kill()