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


class RockCreature(Beetle):
    """A camoflauged creature from the depths"""

    challenge_rating = 2
    splatter_img = pygame.image.load(asset("enemies/splat_brown.png"))
    def __init__(self, game, objT):
        super().__init__(game, objT)

    def set_stats(self):
        self.health = 75
        
        self.vel = Vec(2,0)
        self.speed = 1500
        self.rot_speed = 0.03

        self.attack_range = 3500
        self.attack_delay = 200
        self.aggro_range = 30000
        self.debug_render = []
    
    def make_body(self):
        self.angle = -135
        # self.chain = SimpleChain(game, self, 3, [15, 18])
        self.chain = util.Chain(self.game, self, 2, (self.objT.x, self.objT.y), 10, 20, self.head_movement, ball_weight = 6000)
        self.chain.pos = self.pos
        self.last_ouch = 0
        # self.particles = fx.SlowGlowParticles(self.game)

        names = ["head", "head_attack", "body"]
        self.images = [
           pygame.image.load(asset("enemies/rock creature/rock_creature_" + name + ".png")) for name in names 
        ]
        self.animations = [
            Animator({"static": self.images[0], "attack": self.images[1]}, hide=True),
            Animator({"static": self.images[2]}),
        ]
        self.animations[0].set_callback("attack", self.deal_damage)
        
        self.rect = pygame.Rect(0, 0, 20, 20)

    def make_legs(self):
        self.legs = [] 

    def get_state(self):
        match self.state:
            case "aggro":
                pos = self.chain.balls[0].body.position
                if util.distance_squared(pos, self.game.player.body.position) > self.aggro_range+10000:
                    self.state = "searching"
                    self.animations[0].hide = True
                    for a in self.animations:
                        a.clear_fx()
            case "searching":
                pos = self.chain.balls[0].body.position
                if util.distance_squared(pos, self.game.player.body.position) < self.aggro_range:
                    self.aggravate()
            case "attack":
                if now() - self.last_attack > self.attack_delay:
                    self.animations[0].set_mode("attack")
                else:
                    self.animations[0].set_mode("static")
    
    def head_movement(self, body, gravity, damping, dt):

        match self.state:
            case "aggro":
                old_vel = Vec(body.velocity)
                pos = body.position
                if util.distance_squared(pos, self.game.player.rect.center) > self.attack_range:
                    vel = (self.game.player.rect.center - Vec(pos)).normalize()*self.speed
                    vel = old_vel.lerp(vel, self.rot_speed)
                    vel.scale_to_length(min(vel.length(), self.speed*dt*1000))
                    self.angle = vel.as_polar()[1]
                    body.velocity = tuple(vel)
                else:
                    self.state = "attack"
            case "searching":
                body.velocity = (0, 0)
            case "attack":
                if util.distance_squared(body.position, self.game.player.rect.center) > self.attack_range:
                    self.state = "aggro"
                    self.animations[0].set_mode("static")
                    self.animations[0].framex = 0

    def update_legs(self):
        pass

    def take_damage(self, dmg):
        if not self.state == "searching":
            super().take_damage(dmg)

    def aggravate(self):
        super().aggravate()
        self.animations[0].hide = False
    
    def deal_damage(self):
        super().deal_damage()
        print("yya")
