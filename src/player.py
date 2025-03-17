import util
import math
from time import time

import pygame
from pygame import Vector2
from animations import *
from objects import Wall, Chest
from stgs import *
from overlay import transparent_rect
import fx
import stats
from inventory import Inventory
import items


#### Player object ####
class Player(util.Sprite):
    '''The Player Object'''
    #### Player Initializations ####
    def __init__(self, game, image, **kwargs):
        '''Loads most of the heavy data for the player here'''
        # Modifiers
        self.hitCooldown = 200
        self.vel = Vector2(0, 0)
        self.speed = 90
        self.speedLim = 7
        self.drag = 0.85
        self.damage = 10
        self.roomBound = True
        self.imgSheet = {"default": asset('player', 'samplePlayer.png'), 'hit':asset('player', 'playerHit1.png'), 'wand':asset('player', 'playerHit1.png')}
        self.width, self.height = 42, 42
        self.health = 50
        self.healthAccumulator = 0
        self.inventory = Inventory()

        ########################
        # This is just for now #
        ########################
        self.sword = items.Sword()
        self.great_sword = items.GreatSword()
        self.dagger = items.Dagger()
        self.inventory.add_item(self.sword)
        self.inventory.add_item(self.great_sword)
        self.inventory.add_item(self.dagger)
        self.equippedWeapon = self.sword; 

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
        self.lastTimeTookDamage = 0
        self.healDelay = 3
        self.mask = pygame.mask.from_surface(self.image, True)
        self.angle = 0
        self.lightImg = pygame.image.load(asset('objects', 'light2.png'))
        self.lightScale = pygame.Vector2(self.lightImg.get_width(), self.lightImg.get_height())
        self.lightScale.scale_to_length(1000)
        self.lightSource = pygame.transform.scale(self.lightImg, (int(self.lightScale.x), int(self.lightScale.y))).convert_alpha()
        self.particleFx = fx.PlayerParticles(self.game, self)
        self.combatParts = fx.CombatParticles(game, self)

        self.attackState = None

        if joystickEnabled:
            self.cursor = Cursor()

        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        self.loadAnimations()
        #self.imgSrc = pygame.transform.scale(self.imgSrc, (int(self.image.get_width()*2), int(self.image.get_height()*2)))

    def loadAnimations(self):
        self.animations = PlayerAnimation(self)
        self.animations.delay = 30

    #### Updates player ####
    def update(self):
        if time() - self.lastTimeTookDamage > self.healDelay:
            self.healthAccumulator += self.game.dt()
        if self.healthAccumulator > 1:
            if self.stats.health < 50:
                self.stats.health += 0.1 * (50 - self.stats.health)
            self.healthAccumulator = 0
        self.move()
        self.setAngle()
        self.checkActions()
        self.animations.update()
        self.weaponCollisions()
        if joystickEnabled:
            self.cursor.update()

    def checkActions(self):
        # Get the current time
        now = pygame.time.get_ticks()
        
        # Setup the actions
        action1, action2 = None, None

        # Check for a joystick
        if joystickEnabled:
            action1 = getJoy1().get_axis(5) > 0
            action2 = getJoy1().get_axis(4) > 0
        else:
            # Mouse

            # Get the pressed buttons
            pressed_buttons = pygame.mouse.get_pressed()
            
            # Update the actions
            action1 = pressed_buttons[0]
            action2 = pressed_buttons[2] 

        if action1:
            #self.stats.inventory.getSlot(1).action(self)
            self.equippedWeapon.action(self)
        elif action2:
            self.stats.inventory.getSlot(2).action(self)
            
    def weaponCollisions(self):
        if self.attackState == "attack":
            self.animations.setMode("hit")
            self.attackState = None
            self.game.mixer.playFx("swing")
        if self.animations.mode == "hit":
            # Create a list of all close by interactables
            interactables = self.game.groups.getProximitySprites(
                self,
                200,
                groups=[self.game.groups.interactable]
            )

            # Create a list of all close by enemies
            enemies = self.game.groups.getProximitySprites(
                self,
                600,
                groups=[self.game.groups.enemies]
            )

            # Check for an interaction with an interactable
            for entity in interactables:
                # Only deal with entities that have images
                if hasattr(entity, "image"):
                    # Determine the cooldown time
                    cooldown = self.equippedWeapon.stats["attack"]["cooldown"]

                    # Check for the collision
                    if time() - entity.last_interaction_time >= cooldown:
                        if pygame.sprite.collide_mask(self, entity):
                            entity.interact()

            # Check for a hit with an enemy
            for e in enemies:
                # Only deal with enemies that have an image
                if hasattr(e, 'image'):
                    # Check for the collision
                    if pygame.sprite.collide_mask(self, e):
                        # Make sure the timing works
                        if pygame.time.get_ticks() - e.lastHit >= 260:
                            # Determine the amount of damage
                            dmg = self.equippedWeapon.get_attack_damage(self)
                            
                            # Deal the damage
                            e.takeDamage(dmg[0])

                            # Make some nice particles
                            self.combatParts.particle(
                                Vector2(e.rect.center),
                                dmg[0],
                                dmg[1]
                            )
    
    def takeDamage(self, damage):
        if pygame.time.get_ticks() - self.lastHit >= self.hitCooldown:
            self.lastTimeTookDamage = time()
            self.stats.health -= damage
            self.lastHit = pygame.time.get_ticks()
            self.game.mixer.playFx('pHit')
            self.animations.fx(HurtFx())
    
    def setAngle(self):
        if joystickEnabled:
            mPos = Vector2(self.cursor.pos)
        else:
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
        # Apply motion based on user input
        if joystickEnabled:
            self.vel.x += self.speed*getJoy1().get_axis(0)* self.game.dt()
            self.vel.y += self.speed*getJoy1().get_axis(1)* self.game.dt()
        else:
            if checkKey('pRight'):
                self.vel.x += self.speed*self.game.dt()
            if checkKey('pLeft'):
                self.vel.x -= self.speed*self.game.dt()
            if checkKey('pUp'):
                self.vel.y -= self.speed*self.game.dt()
            if checkKey('pDown'):
                self.vel.y += self.speed*self.game.dt()
        # Limit
        lim = self.speedLim * self.game.dt2()
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
        self.vel = self.vel * self.drag

    #### Collide checker for player ####
    def collideCheck(self):
        returnVal = False
        for obj in self.game.groups.colliders:
            if isinstance(obj, (Wall, Chest)):
                if self.moveRect.colliderect(obj.rect):
                    returnVal = obj.rect  
            # else:
            #     if pygame.sprite.collide_circle(self, obj):
            #         return obj.getCollider()

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
        cutHole = transparent_rect((50, 50), 0)
        img2.blit(cutHole, cutHole.get_rect(center=self.image.get_rect().center), special_flags=pygame.BLEND_MULT)
        self.mask = pygame.mask.from_surface(img2)
        #return img2

class Cursor:
    def __init__(self, xy=(500, 1)):
        self.pos = Vector2(xy)
        self.speed = 25
        self.size = Vector2(6, 6)
    
    def update(self):
        movex = self.speed*getJoy1().get_axis(2)* self.game.dt()
        movey = self.speed*getJoy1().get_axis(3)* self.game.dt()
        self.pos.x += movex if abs(getJoy1().get_axis(2)) > 0.5 else 0
        self.pos.y += movey if abs(getJoy1().get_axis(3)) > 0.5 else 0
        
        self.pos.x = max(0, min(self.pos.x, winWidth-self.size.x))
        self.pos.y = max(0, min(self.pos.y, winHeight-self.size.y))
