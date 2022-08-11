import pygame
from .enemy import Enemy
from stgs import *
import animations

class Bat(Enemy):
    """A bat enemy"""
    def __init__(self, game, objT):
        super().__init__(game, objT)
        self.health = 20
        self.speed = 2 * deltaConst
        self.damage = 1
        self.attackDelay = 60
        self.width = 48
        self.height = 48
        self.wingChangeDelay = 60
        self.lastWingChange = now()
        self.wingState = 0
        self.wingStates = [
            "down",
            "out"
        ]
        self.lastWingChange = now()
        self.wingImages = []
        for wingState in self.wingStates:
            self.wingImages.append(
                pygame.transform.scale(pygame.image.load(asset("enemies", "bat", "bat_wings_" + wingState + ".png")).convert_alpha(), (self.width, self.height))
            )
        self.setWingImage()
    def setWingImage(self):
        # Load the image
        self.image = self.wingImages[self.wingState]
        self.origImage = self.image.copy()
        # Rotate the image
        self.setAngle()
    def update(self):
        super().update()
        # Move towards the player
        self.move()
        # Change wing image
        if now() - self.lastWingChange >= self.wingChangeDelay:
            self.wingState = (self.wingState + 1) % len(self.wingStates)
            self.setWingImage()
            self.lastWingChange = now()
        self.animations.update()
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
                    self.game.player.takeDamage(5)
        self.image = pygame.transform.rotate(self.origImage, self.angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)
    