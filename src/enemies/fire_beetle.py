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


class FireBeetle(Beetle):
    """A fiery beetle. Medium defensive high damage but low speed"""

    challenge_rating = 2
    splatter_img = pygame.image.load(asset("enemies/splat_red.png"))
    def head_movement(self, body, gravity, damping, dt):
        if self.state == "attack":
            self.state = "aggro"
            speed = self.speed
            self.speed = speed*0.3
            super().head_movement(body, gravity, damping, dt)
            self.speed = speed
            self.state = "attack"
            super().head_movement(body, gravity, damping, dt)
        else:
            super().head_movement(body, gravity, damping, dt)
    def __init__(self, game, objT):
        super().__init__(game, objT)

    def set_stats(self):
        self.health = 150
        
        self.vel = Vec(2,0)
        self.speed = 1400
        self.rot_speed = 0.03

        self.attack_range = 250
        self.aggro_range = 75000
        self.attack_delay = 1800
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
           pygame.image.load(asset("enemies/fire beetle/" + name + ".png")) for name in names 
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
 
    def get_state(self):
        pos = self.chain.balls[0].body.position
        match self.state:
            case "aggro":
                if util.distance_squared(pos, self.game.player.body.position) > 100000:
                    self.state = "searching"
                    for a in self.animations:
                        a.clear_fx()
            case "searching":
                if util.distance_squared(pos, self.game.player.body.position) < self.aggro_range:
                    self.aggravate()
                if self.pause <= 0:
                    if util.distance_squared(pos, self.wander_destination) < 2400:
                        self.pause = 60
                        self.get_wander_destination()
                self.pause -= 1
            case "attack":
                if now() - self.last_attack > self.attack_delay:
                    self.animations[0].set_mode("attack")
                    self.game.get_prefab("EnemyFireball")(self.game, pos, self.game.player.rect.center-pos)
                    self.last_attack = now()
                else:
                    self.animations[0].set_mode("static")

