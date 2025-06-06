import random
from pygame.math import Vector2
import pygame
import math
import numpy as np
from pygame import Vector2 as Vec
from src.stgs import *
import src.fx as fx
import src.stats as stats
from .enemy import SimpleEnemy
from src import util
from src.animations import Animator, HurtFx
from .leg import Leg

class Beetle(SimpleEnemy):
    """A spider sprite with cool top down movement
    """

    def __init__(self, game, objT):
        super().__init__(game, objT)

        self.health = 100
        
        self.vel = Vec(2,0)
        self.speed = 1700
        self.rot_speed = 0.03

        self.attack_range = 25
        self.debug_render = []

        self.make_legs()

        self.angle = -135
        # self.chain = SimpleChain(game, self, 3, [15, 18])
        self.chain = util.Chain(game, 3, (objT.x, objT.y), 8.4, 12, self.head_movement)
        self.chain.pos = self.pos
        self.last_ouch = 0
        # self.particles = fx.SlowGlowParticles(self.game)

        names = ["head", "body", "butt"]
        self.images = [
           pygame.image.load(asset("enemies/beetle/beetle_" + name + ".png")) for name in names 
        ]
        self.animations = [
            Animator({"static": self.images[0]}),
            Animator({"static": self.images[1]}),
            Animator({"static": self.images[2]}),
        ]
        
        self.rect = pygame.Rect(0, 0, 20, 20)
        
        # Used for managing the state of the beetle
        #
        # Creep - The beetle is walking toward the player
        #
        self.state = "searching"
        self.pause = 0
        self.get_wander_destination()

    def make_legs(self):
        self.leg_mounts = [0 for i in range(6)]
        self.feet = [0 for i in range(6)]
        self.feet_dist_x = 1
        self.feet_dist_y = 11
        # self.legs = [Leg((0,0), (15,0)) for i in range(6)]
        self.legs = [Leg(11) if i % 2 else Leg(-11) for i in range(6)]
        self.legs[0].radius = 5
        self.legs[1].radius = 5
        self.legs[2].radius = 5
        for l in self.legs:
            l.color = (143, 200, 215)
            l.speed = self.speed/300
        self.offset = Vec(-15, 0)
        self.phase_offset = 15
        self.phases = [True, False, False, True, True, False]
        self.travel = 2.2
        
    def update(self):
        super().update()
        # self.move()
        # self.rect.center = self.body.position
        self.chain.update()
        self.update_legs()
        self.get_state()
        # self.particles.update_position(self.rect.center)
        
        for a in self.animations:
            a.update()
    
    def get_state(self):
        match self.state:
            case "creep":
                pass
            case "searching":
                pos = self.chain.balls[0].body.position
                if util.distance_squared(pos, self.game.player.body.position) < 20000:
                    self.state = "creep"
                if self.pause <= 0:
                    if util.distance_squared(pos, self.wander_destination) < 1800:
                        self.pause = 60
                        self.get_wander_destination()
                self.pause -= 1

    def get_wander_destination(self):
        # Finds a suitable place for the beetle to wander to
        level_w, level_h = self.game.map.floor.room.rect.size
        self.wander_destination = (random.random()*level_w, random.random()*level_h)
                
    def head_movement(self, body, gravity, damping, dt):
        match self.state:
            case "creep":
                old_vel = Vec(body.velocity)
                pos = body.position
                if util.distance(pos, self.game.player.rect.center) > self.attack_range:
                    vel = (self.game.player.rect.center - Vec(pos)).normalize()*self.speed
                    vel = old_vel.lerp(vel, self.rot_speed)
                    vel.scale_to_length(min(vel.length(), self.speed*dt*1000))
                    self.angle = vel.as_polar()[1]
                    body.velocity = tuple(vel)
            case "searching":
                old_vel = Vec(body.velocity)
                pos = body.position
                if util.distance(pos, self.wander_destination) > 50:
                    vel = (self.wander_destination - Vec(pos)).normalize()*self.speed*0.4
                    vel = old_vel.lerp(vel, self.rot_speed)
                    vel.scale_to_length(min(vel.length(), self.speed*dt*2))
                    self.angle = vel.as_polar()[1]
                    body.velocity = tuple(vel)


    def update_legs(self):
        i=0
        for c in self.chain.get_points():
            c = Vec(c)
            angle = self.angle if i == 0 else self.chain.chain_angles[int(i/2)] + 180
            # Distance from center of segment
            dist = Vec(1, 0).rotate(angle)*10
            
            # place the leg on the side of segment and place foot
            leg_mount = c + dist.rotate(-90)
            foot = c + dist.rotate(-90) * self.travel + dist*self.travel*0.5 #Place further out
            self.legs[i].update(leg_mount, foot, dist, self.phase_offset if self.phases[i] else 1)
            self.leg_mounts[i] = leg_mount
            self.feet[i] = foot
            
            i += 1
            # Repeat for other side of segment
            leg_mount = c + dist.rotate(90)
            foot = c + dist.rotate(90) * self.travel + dist*self.travel*0.5
            self.legs[i].update(leg_mount, foot, dist, self.phase_offset if self.phases[i] else 1)
            self.leg_mounts[i] = leg_mount
            self.feet[i] = foot
            i += 1

    def get_colliders(self, type="circle"):
        return self.chain.get_colliders(type)

    def draw(self, surf, transform=None):
        for l in self.legs:
            l.draw(surf, transform)

        chain_points = self.chain.get_points()
        rects = []
        imgs = []
        for i in range(len(self.images)):
            angle = -self.chain.chain_angles[i] + 90 if i > 0 else -self.angle - 90
            image = pygame.transform.rotate(self.animations[i].get_image(), angle)
            rect = image.get_rect(center = chain_points[i])

            surf.blit(image, transform(rect))
            
            rects.append(rect)
            imgs.append(image)

        # The draw function is quite intensive because as well as finding the screen position
        # It needs to create an image for the sprite because the game relies on mask 
        # Collision. Right here we adjust the position of the elements in the chain to 
        # Calculate where to put the mask
        min_x, min_y, max_x, max_y = *rects[0].topleft,0,0
        for r in rects:
            min_x = min(min_x, r.topleft[0])
            min_y = min(min_y, r.topleft[1])
            max_x = max(max_x, r.bottomright[0])
            max_y = max(max_y, r.bottomright[1])
        size = (max_x - min_x, max_y - min_y)
        self.rect = pygame.Rect(min_x, min_y, *size) 
        self.image = pygame.Surface(size)

        for i in range(len(imgs)):
            self.image.blit(imgs[i], Vec(rects[i].topleft) - rects[0].topleft)
        
        if DEBUG_RENDER:
            if not isinstance(self.feet[0], int):
                for f in self.feet:
                    f = pygame.Rect(*f, 1, 1)
                    pygame.draw.circle(surf, util.white, transform(f).center, 2)

                for f in self.leg_mounts:
                    f = pygame.Rect(*f, 1, 1)
                    pygame.draw.circle(surf, util.white, transform(f).center, 2)

            if self.debug_render:
                a = self.game.cam.applyVec(self.debug_render[0])
                b = self.game.cam.applyVec(self.debug_render[1])

                pygame.draw.line(surf, util.white, a, b)

    def take_damage(self, dmg):
        super().take_damage(dmg)
        for a in self.animations:
            a.fx(HurtFx())

    def take_knockback(self, player):
        head = self.chain.balls[0].body
        diff = Vec(head.position) - Vec(player.body.position)
        self.debug_render = [head.position, player.body.position]
        diff.scale_to_length(head.mass*20*player.slot1._weight)
        for b in self.chain.balls:
            b.body.apply_impulse_at_local_point(tuple(diff), (0, 0))
        # self.chain.balls[-1].body.apply_impulse_at_local_point(tuple(diff), (0, 0))

    def kill(self):
        super().kill()
        self.chain.kill()
        # self.particles.kill()
