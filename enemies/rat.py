import pygame
from .enemy import Enemy
from stgs import *
import animations

class Rat(Enemy):
    """A rat enemy"""
    def __init__(self, game, objT):
        super().__init__(game, objT)
        self.health = 5
        self.damage = 1
        self.width = 48
        self.height = 48
        self.angle = 0
        self.speed = 4
        self.vel = pygame.Vector2(0, 0)
        self.image = pygame.transform.scale(pygame.image.load(asset("enemies", "rat", "rat.png")).convert_alpha(), (self.width, self.height))
        self.origImage = self.image.copy()
        self.rect = pygame.Rect(objT.x, objT.y, self.width, self.height)
        self.animations = animations.Animation(self)
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
                if now() - self.lastAttack >= self.attackDelay:
                    self.game.player.takeDamage(5)
        self.image = pygame.transform.rotate(self.origImage, self.angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)
    def collideCheck(self, vector):
        testRect = pygame.Rect(0, 0, 32, 32)
        testRect.center = vector
        for obj in self.game.groups.colliders:
            if testRect.colliderect(obj.rect) and not obj == self:
                return True
        
        return False
    def move(self):
        """Move the rat"""
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
    def update(self):
        super().update()
        # Move towards the player
        self.move()
        self.animations.update()
    def kill(self):
        super().kill()