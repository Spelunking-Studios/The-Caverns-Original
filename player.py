#### Imports ####

import math

import pygame
from pygame import Vector2
from animations import *
from objects import *
from stgs import *
import fx


#### Player object ####
class player(pygame.sprite.Sprite):
    x = 71
    y = 71
    yModMin = -0.12
    yModMax = 0.25
    hitCooldown = 500
    lastHit = 0
    roomBound = True
    imgSheet = {'active': False, 'tileWidth': 64, 'r': False, 'l': False, 'idleR': False, 'flyR': False, 'flyL': False}
    width, height = 48, 48
    health = 50
    maxHp = 50
    attempts = 0
    #### Player Initializations ####
    def __init__(self, game, image, name, **kwargs):
        self.groups = [game.sprites, game.layer2]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pygame.image.load(image)
        self.imgSrc = self.image.copy()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.moveRect = self.rect.copy()
        self.vel = Vector2(0, 0)
        self.speed = 1
        self.drag = 0.80
        self.damage = 10
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
        pass
        #self.animations = animation(self)
        #self.animations.scale(2, 3)
        #self.animations.rotation = True

    #### Updates player ####
    def update(self):
        self.move()
        self.setAngle()
        #self.animations.update()
    
    def takeDamage(self, damage):
        if pygame.time.get_ticks() - self.lastHit >= self.hitCooldown:
            self.health -= damage
            self.lastHit = pygame.time.get_ticks()
            self.game.mixer.playFx('pHit')
    
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
        self.rotCenter()

    def rotCenter(self, angle=False):
        if not angle:
            angle = self.angle
        self.image = pygame.transform.rotate(self.imgSrc, angle)
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
            #if isinstance(obj, rebound):
                    #if self.maskCollide(obj.rect):
            if self.moveRect.colliderect(obj.rect):
                returnVal = obj.rect  
            
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
