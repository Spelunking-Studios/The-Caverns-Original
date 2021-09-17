#### Imports ####

import math

import pygame
from pygame import Vector2
from animations import *
from objects import *
from stgs import *
from overlay import transparentRect
import fx
import stats


#### Player object ####
class player(pygame.sprite.Sprite):
    
    #### Player Initializations ####
    def __init__(self, game, image, **kwargs):
        # Modifiers
        self.hitCooldown = 500
        self.vel = Vector2(0, 0)
        self.speed = 1
        self.drag = 0.80
        self.damage = 10
        self.roomBound = True
        self.imgSheet = {"default": asset('player//samplePlayer.png'), 'hit':asset('player/playerHit1.png')}
        self.width, self.height = 42, 42
        self.health = 50

        self.groups = [game.sprites, game.layer2]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pygame.image.load(image)
        self.imgSrc = self.image.copy()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.moveRect = self.rect.copy()
        self.stats = stats.PlayerStats()
        self.lastHit = 0
        self.lastAttack = 0
        self.mask = pygame.mask.from_surface(self.image, True)
        self.angle = 0
        self.lightImg = pygame.image.load(asset('objects/light2.png'))
        self.lightScale = pygame.Vector2(self.lightImg.get_width(), self.lightImg.get_height())
        self.lightScale.scale_to_length(1000)
        self.lightSource = pygame.transform.scale(self.lightImg, (int(self.lightScale.x), int(self.lightScale.y))).convert_alpha()
        self.particleFx = fx.playerParticles(self.game, self)

        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        self.loadAnimations()
        #self.imgSrc = pygame.transform.scale(self.imgSrc, (int(self.image.get_width()*2), int(self.image.get_height()*2)))

    def loadAnimations(self):
        self.animations = playerAnimation(self)
        self.animations.delay = 30

    #### Updates player ####
    def update(self):
        self.move()
        self.setAngle()
        self.checkActions()
        self.animations.update()
        self.weaponCollisions()

    def checkActions(self):
        now = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0]:
            self.stats.inventory.getSlot(1).action(self)
        elif pygame.mouse.get_pressed()[2]:
            self.stats.inventory.getSlot(2).action(self)
            
            
    def weaponCollisions(self):
        if self.animations.mode == "hit":
            for e in self.game.enemies:
                if hasattr(e, 'image'):
                    if pygame.sprite.collide_mask(self, e):
                        if pygame.time.get_ticks() - e.lastHit >= 260:
                            e.takeDamage(self.stats.attack())
                        #print(e.health)
    
    def takeDamage(self, damage):
        if pygame.time.get_ticks() - self.lastHit >= self.hitCooldown:
            self.health -= damage
            self.lastHit = pygame.time.get_ticks()
            self.game.mixer.playFx('pHit')
            self.animations.fx(hurtFx())
    
    def setAngle(self):
        mPos = pygame.Vector2(pygame.mouse.get_pos())  ## Gets mouse position and stores it in vector. This will be translated into the vector that moves the bullet
        pPos = self.game.cam.apply(self)  ## Gets actual position of player on screen
        mPos.x -= pPos.centerx ## Finds the x and y relativity between the mouse and player and then calculates the offset
        mPos.y -= pPos.centery
        try:
            self.angle = math.degrees(math.atan2(-mPos.normalize().y, mPos.normalize().x))
        except ValueError:
            self.angle = 0
        self.angle -= 90
        # self.rotCenter()

    def rotCenter(self, angle=False):
        if not angle:
            angle = self.angle
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)
        self.mask = pygame.mask.from_surface(self.image, True)
    
    def spin(self):
        self.angle += self.spinSpeed

    #### Move Physics ####
    def move(self):
        if checkKey('pRight'):
            self.vel.x += self.speed
        if checkKey('pLeft'):
            self.vel.x -= self.speed
        if checkKey('pUp'):
            self.vel.y -= self.speed
        if checkKey('pDown'):
            self.vel.y += self.speed

        lim = 8
        if self.vel.length() > 0.1: # We can't limit a 0 vector 
            self.vel.scale_to_length(max(-lim,min(self.vel.length(),lim)))

            self.moveRect.x += round(self.vel.x)
            collide = self.collideCheck()
            if collide:
                if self.vel.x > 0:
                    self.moveRect.right = collide.left
                else: 
                    self.moveRect.left = collide.right
                self.vel.x = 0
            
            self.moveRect.y += round(self.vel.y)
            collide = self.collideCheck()
            if collide:
                if self.vel.y > 0:
                    self.moveRect.bottom = collide.top
                else: 
                    self.moveRect.top = collide.bottom
                self.vel.y = 0

            self.particleFx.hide = False
        else:
            self.vel = Vector2(0, 0)
            self.particleFx.hide = True

        self.rect.center = self.moveRect.center
        self.vel = self.vel*self.drag

    #### Collide checker for player ####
    def collideCheck(self):
        returnVal = False
        for obj in self.game.colliders:
            if isinstance(obj, wall):
                if self.moveRect.colliderect(obj.rect):
                    returnVal = obj.rect  
            else:
                if pygame.sprite.collide_circle(self, obj):
                    return obj.getCollider()

        return returnVal
    
    def maskCollide(self, rect2):
        r2 = rect2
        return self.mask.overlap(pygame.mask.Mask(r2.size, True), (r2.x-self.moveRect.x,r2.y-self.moveRect.y))
    
    def setPos(self, tup, center=False):
        self.vel = Vector2(0, 0)
        if center:
            self.moveRect.center = tup
        else:
            self.moveRect.topleft = tup
        self.rect = self.moveRect.copy()
    
    def getAttackMask(self):
        img2 = self.image.copy()
        img2.set_colorkey((0, 0, 0))
        cutHole = transparentRect((50, 50), 0)
        img2.blit(cutHole, cutHole.get_rect(center=self.image.get_rect().center), special_flags=pygame.BLEND_MULT)
        self.mask = pygame.mask.from_surface(img2)
        return img2