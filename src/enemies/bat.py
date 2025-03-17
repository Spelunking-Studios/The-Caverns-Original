import pygame
from .enemy import Enemy
from stgs import *
import animations
import random
import time
# from beziation import bezier

def utime():
    return int(time.time())

class Bat(Enemy):
    """A bat enemy"""
    def __init__(self, game, objT):
        super().__init__(game, objT)
        self.health = 20
        self.speed = 170
        self.damage = 1
        self.attackDelay = 60
        self.detectionRange = 500
        self.width = 32
        self.height = 32
        # Attack behaviour
        self.attacking = False
        self.attack = {
            "startPos": None,
            "playerPos": None,
            "cachedPlayerPos": None,
            "endPos": None,
            "reachedPlayer": False,
            "bezierCurve": None,
            "last": 0,
            "delay": 60,
            "target": None
        }
        # Wing animation
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
                pygame.transform.scale(
                    pygame.image.load(
                        asset("enemies", "bat", "bat_wings_" + wingState + ".png")
                    ).convert_alpha(), (self.width, self.height)
                )
            )
        self.setWingImage()
    def setWingImage(self):
        """Sets the bat's wing image"""
        # Load the image
        self.image = self.wingImages[self.wingState]
        self.origImage = self.image.copy()
        # Rotate the image
        self.rotateImage()
    def update(self):
        super().update()
        if self.active:
            if not self.attacking:
                if utime() - self.attack["last"] > self.attack["delay"]:
                    self.startAttack()
            self.attemptToDealDamage()
        # Move towards the player
        self.move()
        #print(self.angle, self.attack, self.attacking)
        # Change wing image
        if now() - self.lastWingChange >= self.wingChangeDelay:
            self.wingState = (self.wingState + 1) % len(self.wingStates)
            self.setWingImage()
            self.lastWingChange = now()
        self.animations.update()
    def startAttack(self):
        """Creates all of the necesary values for the bat to begin its attack"""
        self.attack["last"] = utime()
        self.attack["startPos"] = pygame.Vector2(self.rect.center)
        self.attack["playerPos"] = pygame.Vector2(self.game.player.rect.center)
        self.attack["cachedPlayerPos"] = self.attack["playerPos"]
        self.pickEndPos(pickRandom = True)
        self.attack["target"] = self.attack["playerPos"]
        self.attacking = True
    def endAttack(self):
        """Resets all of the necessary values to effectivly end the attack"""
        self.attack["reachedPlayer"] = False
        self.attacking = False
    def pickEndPos(self, angle = 0, pickRandom = False):
        """Picks the end position for the bat's attack.
        It can use a provided angle or the angle can be randomly selected"""
        if pickRandom:
            angle = random.randint(0, 360)
        ev = pygame.Vector2()
        ev.from_polar((100, (angle) % 360))
        ev.x += self.pos.x
        ev.y += self.pos.y
        ev.x = int(ev.x)
        ev.y = int(ev.y)
        self.attack["endPos"] = ev
        return ev
    def getDistFromPlayer(self):
        mPos = pygame.Vector2(self.game.player.rect.center)
        pPos = self.rect
        mPos.x -= pPos.centerx
        mPos.y -= pPos.centery
        return mPos.length()
    def move(self):
        """Move the bat"""
        if not self.attacking and not self.active:
            return
        # dt = self.game.clock.get_time() / 1000
        testVec = pygame.Vector2(self.pos)
        testVec.x += self.vel.x * self.speed* self.game.dt()
        if not self.collideCheck(testVec):
            self.pos.x += self.vel.x * self.speed* self.game.dt()
        testVec = pygame.Vector2(self.pos)
        testVec.y += self.vel.y * self.speed* self.game.dt()
        if not self.collideCheck(testVec):
            self.pos.y += self.vel.y * self.speed* self.game.dt()
        self.setAngle()
        self.rect.center = self.pos
        # Check if the bat has reached the attack's end position
        if self.vecsAreSemiEqual(self.pos, self.attack["endPos"]):
            self.endAttack()
    def attemptToDealDamage(self):
        """Attempt to deal damage to the player"""
        mPos = pygame.Vector2(self.game.player.rect.center)
        pPos = self.rect
        mPos.x -= pPos.centerx
        mPos.y -= pPos.centery
        if mPos.length() < self.reach and (True or now() >= self.attackDelay + self.lastAttack):
            self.lastAttack = now()
            self.game.player.takeDamage(self.damage)
            self.attack["reachedPlayer"] = True
            #self.pickEndPos(self.angle, pickRandom = True)
    def setAngle(self):
        if self.attacking:
            if not self.attack["reachedPlayer"]:
                self.setAngleFacingTarget(pygame.Vector2(self.game.player.rect.center))
            else:
                self.setAngleFacingTarget(pygame.Vector2(self.attack["endPos"]))
        else:
            self.setAngleFacingTarget(pygame.Vector2(self.game.player.rect.center))
            self.angle -= 90
            mPos = self.pos
            mPos.x -= self.rect.centerx
            mPos.y -= self.rect.centery
            if mPos.length() > 0:
                mPos.normalize_ip()
            testVec = pygame.Vector2(self.pos)
            testVec.x += mPos.x * self.speed
            testVec.y += mPos.y * self.speed
            if self.collideCheck(testVec):
                print(testVec)
            self.vel = pygame.Vector2(0, 0)
    
