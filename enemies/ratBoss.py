from .enemy import Enemy
from .imageSheet import ImageSheet
import pygame
from stgs import asset, now
import math

class RatBoss(Enemy):
    """Rat Boss enemy"""
    def __init__(self, game, objT):
        super().__init__(game, objT)
        self.health = 200
        self.damage = 5
        self.width = 128
        self.height = 128
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
            for i in range(1, self.imagesInfo[k]):
                image = pygame.transform.scale(
                    pygame.image.load(asset("enemies", "rat_boss", f"rat_boss_{int(k)}_{i}.png"))
                        .convert_alpha(),
                    (self.width, self.height)
                )
                self.images.append(image)
        self.image = self.images[self.imageIndex]
        self.origImage = self.image.copy()
    def update(self):
        super().update()
        self.imageAccumulator += self.game.dt()
        if (self.imageAccumulator > 1):
            self.imageIndex = (self.imageIndex + 1) % self.imagesInfo[str(self.stage)]
            self.image = self.images[self.imageIndex]
            self.origImage = self.image.copy()
        if self.active:
            self.move()
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