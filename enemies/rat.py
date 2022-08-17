import pygame
from .enemy import Enemy
from stgs import *
import animations

class Rat(Enemy):
    """A rat enemy"""
    def __init__(self, game, objT):
        super().__init__(game, objT)
        self.health = 20
        self.damage = 5
        self.width = 48
        self.height = 48
        self.angle = 0
        self.speed = 50
        self.attackDelay = 120
        self.image = pygame.transform.scale(pygame.image.load(asset("enemies", "rat", "rat.png")).convert_alpha(), (self.width, self.height))
        self.origImage = self.image.copy()
        self.rect = pygame.Rect(objT.x, objT.y, self.width, self.height)
    def move(self):
        """Move the rat"""
        dt = self.game.clock.get_time() / 1000
        testVec = pygame.Vector2(self.pos)
        testVec.x += self.vel.x * (self.speed * dt)
        if not self.collideCheck(testVec):
            self.pos.x += self.vel.x * (self.speed * dt)
        testVec = pygame.Vector2(self.pos)
        testVec.y += self.vel.y * (self.speed * dt)
        if not self.collideCheck(testVec):
            self.pos.y += self.vel.y * (self.speed * dt)
        self.setAngle()
        self.rect.center = self.pos
    def update(self):
        super().update()
        # Move towards the player
        self.move()
        self.animations.update()
    def kill(self):
        super().kill()