from src import util
import math
from time import time

import pygame, pymunk
from pygame import Vector2
from src.animations import *
from src.objects import Wall, Chest
from src.stgs import *
from src.overlay import transparent_rect
from src import fx
from src import stats
from src.inventory import Inventory
from src import items


#### Player object ####
class Player(util.Sprite):
    '''The Player Object'''
    #### Player Initializations ####
    def __init__(self, game, saved_inventory=None, equipped_weapon=None, **kwargs):
        '''Loads most of the heavy data for the player here'''
        # Modifiers
        self.hitCooldown = 200
        self.damage = 10
        self.roomBound = True
        self.imgSheet = {"default": asset('player', 'player.png'), 
                         'run': asset('player', 'player_running.png'), 
                         'hit':asset('player', 'player_hitting.png'), 
                         'hit_mask':asset('player', 'player_hitting_mask.png'), 
                         'wand':asset('player', 'playerHit1.png')
                         }
        self.width, self.height = 42, 42
        self.health = 50
        self.healthAccumulator = 0
        self.inventory = Inventory()

        
        if DEBUG:
            self.sword = items.Sword()
            self.great_sword = items.GreatSword()
            self.dagger = items.Dagger()
            self.axe = items.Axe()
            self.inventory.add_item(self.sword)
            self.inventory.add_item(self.great_sword)
            self.inventory.add_item(self.dagger)
            self.inventory.add_item(self.axe)
            self.inventory.add_item(items.Mace())
            self.inventory.add_item(items.ThrowingKnives())
            self.slot1 = self.sword
            self.slot2 = items.Wand()
        else:
            if saved_inventory is None:
                # What you start the game with
                self.slot1 = items.Dagger()
                self.inventory.add_item(self.slot1)
            else:
                self.inventory.deserialize(saved_inventory)

                if equipped_weapon:
                    self.slot1 = self.inventory.get_item(equipped_weapon)
                else:
                    self.slot1 = items.Dagger()
            self.slot2 = None
        self.groups = [game.sprites, game.layer2, game.groups.players]
        super().__init__(self.groups)

        self.game = game
        self.loadAnimations()
        self.image = self.animations.getFirstFrame()
        self.imgSrc = self.image.copy()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.moveRect = self.rect.copy()
        self.stats = stats.PlayerStats(self)

        # Timing variables
        self.lastHit = 0
        self.lastAttack = 0
        self.lastTimeTookDamage = 0
        self.using_stamina = False
        self.interacted = False
        self.healDelay = 3
        self.light_size = 1000
        self.darkened_size = 500
        self.dark_recovery_speed = 3

        self.mask = pygame.mask.from_surface(self.image, True)
        self.angle = 0
        self.lightImg = pygame.image.load(asset('objects', 'light4.png')).convert_alpha()
        self.lightScale = pygame.Vector2(self.lightImg.get_width(), self.lightImg.get_height())
        self.lightScale.scale_to_length(self.light_size)
        self.lightSource = pygame.transform.scale(self.lightImg, (int(self.lightScale.x), int(self.lightScale.y))).convert_alpha()
        self.particleFx = fx.PlayerParticles(self.game, self)
        self.combatParts = fx.CombatParticles(game, self)
        self.healthParts = fx.CombatParticles(game, self)
        self.healthParts.partColor = util.green

        self.attackState = None
        # Checks whether player used right or left click last 
        self.last_action = None

        if joystickEnabled:
            self.cursor = Cursor()

        for k, v in kwargs.items():
            self.__dict__[k] = v

        # Load physics
        self.create_physics(
            self.stats.strength*10,
            self.width*0.4,
            self.player_movement,
            (0, 0),
            2
        )
        # self.body.mass = 30000
        
        #self.imgSrc = pygame.transform.scale(self.imgSrc, (int(self.image.get_width()*2), int(self.image.get_height()*2)))

    def loadAnimations(self):
        self.animations = PlayerAnimation(self)

    def player_movement(self, body, gravity, damping, dt):
        speed = self.stats.speed*75
        max_speed = self.stats.speed*100
        damping = 0.85

        vx, vy = 0, 0
        
        self.using_stamina = False
        if self.stats.stamina > 1 and checkKey("sprint"):
            speed *= self.stats.sprint_multiplier
            self.stats.stamina -= 0.2
            self.using_stamina = True
        if checkKey("up"):
            vy -= 1
        if checkKey("down"):
            vy += 1
        if checkKey("left"):
            vx -= 1
        if checkKey("right"):
            vx += 1
        if not (vx, vy) == (0, 0):
            vxy = pymunk.Vec2d(vx, vy)
            vxy = vxy.normalized()*speed*dt
            body.velocity += vxy
            if not self.animations.mode == "hit":
                self.animations.setMode("run")
        body.velocity *= damping

        # if body.velocity.length > max_speed*dt:
        #     body.velocity = body.velocity.normalized()*max_speed*dt

    #### Updates player ####
    def update(self):
        # Health regeneration code
        if not self.using_stamina and self.stats.stamina < self.stats.staminaMax:
            self.stats.stamina += self.game.dt() * 0.1 * (self.stats.staminaMax - self.stats.stamina)
        self.setAngle()
        self.checkActions()
        self.animations.update()
        self.weaponCollisions()
        if joystickEnabled:
            self.cursor.update()

        

        self.rect.center = self.body.position
        self.particleFx.update()

    def get_attack_damage(self):
        return self.slot1.stats["attack"]["damage"]

    def get_attack_cooldown(self):
        return self.slot1.stats["attack"]["cooldown"]

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
            if self.slot1:
                self.slot1.action(self)
            self.last_action = 1
        elif action2:
            if self.slot2:
                self.slot2.action(self)
            self.last_action = 2

    def weaponCollisions(self):
        if self.attackState == "attack":
            self.animations.setMode("hit", 30)
            self.attackState = None
            self.game.mixer.playFx("swing")
        if self.attackState == "shield":
            self.animation.setMode("shield")
        if self.animations.mode == "hit":
            if not self.interacted:
                # Create a list of all close by interactables
                interactables = self.game.groups.getProximitySprites(
                    self,
                    200,
                    groups=[self.game.groups.interactable]
                )

                # Check for an interaction with an interactable
                for entity in interactables:
                    # Only deal with entities that have images
                    if hasattr(entity, "image"):
                        # Determine the cooldown time
                        cooldown = 600

                        # Check for the collision
                        if pygame.sprite.collide_mask(self, entity):
                            entity.interact()
                            self.interacted = True

            # Create a list of all close by enemies
            enemies = self.game.groups.getProximitySprites(
                self,
                600,
                groups=[self.game.groups.enemies]
            )


            # Check for a hit with an enemy
            for e in enemies:
                # Only deal with enemies that have an image
                if hasattr(e, 'image'):
                    # Check for the collision
                    if pygame.sprite.collide_mask(self, e):
                        # Make sure the timing works
                        if pygame.time.get_ticks() - e.last_hit >= 260:
                            # Determine the amount of damage
                            dmg = self.stats.attack()#self.slot1.get_attack_damage(self)

                            # Deal the damage
                            e.take_damage(dmg[0])
                            if True: # Add a condition for knockback
                                e.take_knockback(self)

                            # Make some nice particles
                            self.combatParts.particle(
                                Vector2(e.rect.center),
                                dmg[0],
                                dmg[1]
                            )
        else:
            self.interacted = False

    def take_damage(self, damage):
        if pygame.time.get_ticks() - self.lastHit >= self.hitCooldown:
            self.lastTimeTookDamage = time()
            self.stats.health -= damage
            self.lastHit = pygame.time.get_ticks()
            self.lightScale.scale_to_length(self.darkened_size)
            self.game.mixer.playFx('pHit')
            self.animations.fx(HurtFx())

    def setAngle(self):
        if joystickEnabled:
            mPos = Vector2(self.cursor.pos)
        else:
            mPos = pygame.Vector2(self.game.get_mouse_pos())  ## Gets mouse position and stores it in vector. This will be translated into the vector that moves the bullet
        pPos = self.game.cam.apply(self)  ## Gets actual position of player on screen
        mPos.x -= pPos.centerx ## Finds the x and y relativity between the mouse and player and then calculates the offset
        mPos.y -= pPos.centery
        try:
            self.angle = math.degrees(math.atan2(-mPos.y, mPos.x))
        except ValueError:
            self.angle = 0
        self.angle -= 90
        # self.rotCenter()

    def rotCenter(self, angle=False):
        self.image = self.rot_image(self.image, angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        if self.animations.mode == "hit":
            self.mask = self.animations.get_mask("hit_mask")

    def rot_image(self, img, angle=None):
        angle = self.angle if not angle else angle
        return pygame.transform.rotate(img, self.angle)

    def spin(self):
        self.angle += self.spinSpeed

    def change_health(self, value):
        self.stats.health += value
        self.healthParts.particle(Vector2(self.rect.center), value, False)

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

    def draw_darkness(self, ctx, transform=None):
        if transform:
            dark = self.lightScale.length()
            wobble = math.sin(now()*0.003)*50
            if dark < 1000:
                self.lightScale.scale_to_length(dark + self.dark_recovery_speed)
            self.lightSource = pygame.transform.scale(self.lightImg, (int(self.lightScale.x+wobble), int(self.lightScale.y+wobble)))

            light = self.lightSource
            lightRect = pygame.Rect(0, 0, light.get_width(), light.get_height())
            lightRect.center = transform(self.rect).center
            ctx.blit(light, lightRect)

    def kill(self):
        pass

    # def draw(self, ctx, transform):
    #     super().draw(ctx, transform)
    #     ctx.blit(self.mask.to_surface(), transform(self.rect))


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
