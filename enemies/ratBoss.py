<<<<<<< HEAD
# from socketserver import ThreadingUnixStreamServer
=======
>>>>>>> 82eae6df1d06f692c3572baf1f9b8e081664da1f
from .enemy import Enemy
from .imageSheet import ImageSheet
import pygame
from stgs import asset, now
import math
from effects import HurtEffect

class RatBoss(Enemy):
    """Rat Boss enemy"""
    def __init__(self, game, objT):
        super().__init__(game, objT)
        self.health = 200
        self.damage = 32
        self.width = 128
        self.height = 128
        self.reach = 64
        self.angle = 0
        self.speed = 40
        self.attackDelay = 240
        self.detectionRange = 1000
        self.imageAccumulator = 0
        self.images = []
        self.imageIndex = 1
        self.stage = 1
        self.imagesInfo = {
            "1": 6,
            "2": 4,
            "3": 5
        }
        for k in self.imagesInfo.keys():
            for i in range(1, self.imagesInfo[k] + 1):
                image = pygame.transform.scale(
                    pygame.image.load(asset("enemies", "rat_boss", f"rat_boss_{int(k)}_{i}.png"))
                        .convert_alpha(),
                    (self.width, self.height)
                )
                self.images.append(image)
        self.image = self.images[self.imageIndex]
        self.origImage = self.image.copy()
        self.rect = pygame.Rect(objT.x, objT.y, self.width, self.height)
    def update(self):
        super().update()
        self.imageAccumulator += self.game.dt()
        if (self.imageAccumulator > 0.1):
            if self.stage == 1:
                self.imageOffset = 0
            else:
                ac = 0
                for k in self.imagesInfo.keys():
                    if int(k) >= self.stage:
                        break
                    ac += self.imagesInfo[k]
                self.imageOffset = ac
            self.imageIndex = (self.imageIndex + 1) % self.imagesInfo[str(self.stage)]
            self.imageIndex += self.imageOffset
            self.image = self.images[self.imageIndex]
            self.origImage = self.image.copy()
            self.imageAccumulator = 0
        if self.active:
            self.move()
        self.animations.update()
    def move(self):
        """Move the rat boss"""
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
    def takeDamage(self, damage):
        super().takeDamage(damage)
        healthPercent = int(100 / (200 / self.health))
        if healthPercent > 65:
            self.stage = 1
        elif healthPercent > 25:
            self.stage = 2
        else:
            self.stage = 3