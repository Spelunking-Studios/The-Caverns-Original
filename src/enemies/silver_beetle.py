from pygame.math import Vector2
import pygame
import math
import numpy as np
from pygame import Vector2 as Vec
from src.stgs import *
import src.fx as fx
import src.stats as stats
from .beetle import Beetle
from src import util
from src.animations import Animator, HurtFx
from .leg import Leg


class SilverBeetle(Beetle):
    """A metallic beetle. High defensive but low speed"""

    def __init__(self, game, objT):
        super().__init__(game, objT)

    def set_stats(self):
        self.health = 150
        
        self.vel = Vec(2,0)
        self.speed = 1000
        self.rot_speed = 0.03

        self.attack_range = 25
        self.debug_render = []
    
    def make_body(self):
        self.angle = -135
        # self.chain = SimpleChain(game, self, 3, [15, 18])
        self.chain = util.Chain(self.game, 4, (self.objT.x, self.objT.y), 13, 19, self.head_movement)
        self.chain.pos = self.pos
        self.last_ouch = 0
        # self.particles = fx.SlowGlowParticles(self.game)

        names = ["head", "torso2", "torso1", "butt"]
        self.images = [
           pygame.image.load(asset("enemies/silver beetle/" + name + ".png")) for name in names 
        ]
        self.animations = [
            Animator({"static": self.images[0]}),
            Animator({"static": self.images[1]}),
            Animator({"static": self.images[2]}),
            Animator({"static": self.images[3]}),
        ]
        
        self.rect = pygame.Rect(0, 0, 20, 20)

    def make_legs(self):
        self.leg_mounts = [0 for i in range(8)]
        self.feet = [0 for i in range(8)]
        self.feet_dist_x = 1
        self.feet_dist_y = 20
        # self.legs = [Leg((0,0), (15,0)) for i in range(6)]
        self.leg_length = 22
        self.legs = [Leg(self.leg_length) if i % 2 else Leg(-self.leg_length) for i in range(8)]
        for l in self.legs:
            l.color = util.stone_grey
            l.speed = self.speed/300
        self.offset = Vec(-25, 0)
        self.phase_offset = 15
        self.phases = [True, False, False, True, True, False, False, True]
        self.travel = 3.2
 
