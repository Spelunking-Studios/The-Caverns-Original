import pygame
from .enemy import Enemy
from stgs import *
import animations
import random


# Note to devs:
# The bat's movement is based upon a list of movement points which represent
# the various locations the bat wants to move to.
# 
# To actually reach these points, the bat will follow a curve leading to the 
# different points. 
# 
# The curve uses a bezier curve to determine the points the bat will move to.
# 
# 


class Bat(Enemy):
    """A bat enemy"""
    def __init__(self, game, objT):
        super().__init__(game, objT)
        self.health = 20
        self.speed = 2 * deltaConst
        self.damage = 1
        self.attackDelay = 60
        self.width = 32
        self.height = 32
        # Attack behaviour
        self.attacking = False
        self.attack = {
            "startPos": None,
            "playerPos": None,
            "endPos": None,
            "reachedPlayer": False
        }
        self.movementPoints = [
            list(self.game.player.rect)[:2]
        ]
        self.objectiveComplete = False
        self.attackedPlayer = False
        self.movementSkew = random.randint(-10, 10)
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
                pygame.transform.scale(pygame.image.load(asset("enemies", "bat", "bat_wings_" + wingState + ".png")).convert_alpha(), (self.width, self.height))
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
        # Update the movement points
        self.updateMovementPoints()
        # Move towards the player
        self.move()
        # Attack
        if not self.attacking:
            self.startAttack()
        print(self.angle, self.attack)
        # Change wing image
        if now() - self.lastWingChange >= self.wingChangeDelay:
            self.wingState = (self.wingState + 1) % len(self.wingStates)
            self.setWingImage()
            self.lastWingChange = now()
        self.animations.update()
    def startAttack(self):
        """Creates all of the necesary values for the bat to begin its attack"""
        print("Starting bat attack")
        self.attack["startPos"] = pygame.Vector2(self.rect[:2])
        self.attack["playerPos"] = pygame.Vector2(self.game.player.rect[:2])
        endPosVec = pygame.Vector2()
        endPosVec.from_polar((30, (self.angle) % 360))
        endPosVec.x += self.pos.x
        endPosVec.y += self.pos.y
        self.attack["endPos"] = endPosVec
        self.attacking = True
    def updateMovementPoints(self):
        """Updates the bat's movement points"""
        self.attack["playerPos"] = pygame.Vector2(self.game.player.rect[:2])
        self.attack["cPos"] = self.pos
        if not self.attackedPlayer:
            target = list(self.game.player.rect)[:2]
        else:
            # Re-roll movement skew
            self.movementSkew = random.randint(-10, 10)
            tAngle = (self.game.player.angle + 180) % 360
            print(tAngle)
            vec = pygame.Vector2()
            vec.from_polar((10, tAngle))
            target = [
                self.pos.x + vec.x,
                self.pos.y + vec.y
            ]
        self.movementPoints = [
            [
                target[0] + self.movementSkew,
                target[1]
            ],
            target
        ]
    def move(self):
        """Move the bat"""
        testVec = pygame.Vector2(self.pos)
        testVec.x += self.vel.x * self.speed
        if not self.collideCheck(testVec):
            self.pos.x += self.vel.x * self.speed
        testVec = pygame.Vector2(self.pos)
        testVec.y += self.vel.y * self.speed
        if not self.collideCheck(testVec):
            self.pos.y += self.vel.y * self.speed
        #if not self.attacking:
        #    print(self.attacking)
        self.setAngle()
        self.rect.center = self.pos
        if self.vecsAreEqual(self.pos, self.attack["endPos"]):
            self.attacking = False
    def vecsAreEqual(self, vec1, vec2):
        if not vec1 or not vec2:
            return False
        if int(vec1.x) == int(vec2.x) and int(vec1.y) == int(vec2.y):
            return True
        return False
    def setAngleFacingTarget(self, targetPos):
        """Rotates the bat to face the target position"""
        mPos = targetPos
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
                    self.attackedPlayer = True
                    self.attack["reachedPlayer"] = True
        self.rotateImage()
    def setAngle(self):
        if self.attacking:
            if not self.attack["reachedPlayer"]:
                self.setAngleFacingTarget(pygame.Vector2(self.game.player.rect.center))
            else:
                self.setAngleFacingTarget(self.attack["endPos"])
        else:
            self.setAngleFacingTarget(pygame.Vector2(self.game.player.rect.center))
    def rotateImage(self):
        self.image = pygame.transform.rotate(self.origImage, self.angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)
    