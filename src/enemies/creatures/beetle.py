from pygame.math import Vector2
import pygame
import math
import numpy as np
from pygame import Vector2 as Vec
from src.stgs import *
from src import util
from src.animationsNew import Animator, HurtFx
from .chain import SimpleChain
from .leg import Leg

class Beetle(util.Sprite):
    """A spider sprite with cool top down movement
    """

    def __init__(self, game, objT):
        super().__init__((game.sprites, game.layer1))
        
        self.pos = Vec((objT.x, objT.y))
        self.dir = Vec(2,0)

        self.leg_mounts = [0 for i in range(6)]
        self.feet = [0 for i in range(6)]
        self.feet_dist_x = 13
        self.feet_dist_y = 11
        # self.legs = [Leg((0,0), (15,0)) for i in range(6)]
        self.legs = [Leg(11) if i % 2 else Leg(-11) for i in range(6)]
        for l in self.legs:
            l.color = (143, 200, 215)
            l.speed = self.dir.length()*2
        self.offset = Vec(-15, 0)
        self.phase_offset = 15
        self.phases = [True, False, False, True, True, False]
        self.travel = 2.5
        
        self.angle = -135
        self.chain = SimpleChain(game, 3, [15, 18])
        self.chain.pos = self.pos
        self.last_ouch = 0
        
        names = ["head", "body", "butt"]
        self.images = [
           pygame.image.load(asset("enemies/beetle/beetle_" + name + ".png")) for name in names 
        ]
        self.animations = [
            Animator({"static": self.images[0]}),
            Animator({"static": self.images[1]}),
            Animator({"static": self.images[2]}),
        ]
        
    def update(self):
        self.pos += self.dir
        self.dir.rotate_ip(0.5)
        self.angle = self.dir.as_polar()[1]
        self.chain.pos = self.pos
        self.chain.update()
        self.update_legs()
        
        for a in self.animations:
            a.update()

    def update_legs(self):
        i=0
        for c in self.chain.chain:
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


    def draw(self, surf, transform=None):
        for l in self.legs:
            l.draw(surf, transform)

        for i in range(len(self.images)):
            angle = -self.chain.chain_angles[i] + 90 if i > 0 else -self.angle - 90
            image = pygame.transform.rotate(self.animations[i].get_image(), angle)
            rect = image.get_rect(center = image.get_rect(center = self.chain.chain[i]).center)

            surf.blit(image, transform(rect))
