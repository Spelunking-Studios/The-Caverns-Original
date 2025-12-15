import pygame
from pygame import Vector2 as Vec
import random

from src.animations import Animator
from src.stgs import *
from src import util
from src import fx
from .enemy import SimpleEnemy

from src.util import print_stats

class Bat(SimpleEnemy):
    """A very small and quick bug that catches you by 
    suprise and then Boom
    """

    challenge_rating = 1

    def __init__(self, game, objT):
        super().__init__(game, objT)
        game.groups.bats.add(self)

        self.last_attack = 0
        self.attack_delay = 400

        self.set_stats() 
        self.create_body()
        self.create_physics(10, 5, self.fake_move, self.rect.center, self.collision_type)
        self.charging = False

        self.pos = Vec(self.rect.center)
        self.vel = Vec(0, 0)
    
    @print_stats
    def set_stats(self):
        self.health = 5
        self.speed = 20
        self.angle = 0
        self.rot_speed = 0.01
        self.charge_range = 800
        self.attack_range = 40
        self.boom_range = 50
        self.damage = 3

    def create_body(self):
        self.animations = Animator({
            "flying": pygame.image.load(asset("enemies/bat/bat_flying.png")), 
        }, 60, mode = "flying", transforms = [self.rot_center])
        self.image = self.animations.getFirstFrame()
        self.rect = pygame.Rect(self.objT.x, self.objT.y, *self.image.get_size())
        # self.particles = fx.SlowGlowParticles(self.game, color = util.wheat_gold, speed = 0.5)

    def update(self):
        super().update()
        self.move()
        self.rect.center = tuple(self.pos)
        # self.particles.position = pos

        if now() - self.last_attack > self.attack_delay:
            if util.distance(self.rect.center, self.game.player.rect.center) <= self.attack_range:
                self.attack()

        self.animations.update()
        self.image = self.animations.get_image()

    def attack(self):
        super().deal_damage()
        
    def fake_move(self, body, *args):
        body.position = tuple(self.pos)
    def move(self):
        dt = self.game.dt()
        old_vel = self.vel.copy()
        if util.distance(tuple(self.pos), self.game.player.rect.center) <  self.charge_range:
            self.vel = (self.game.player.rect.center - self.pos).normalize()*self.speed
            self.vel = old_vel.lerp(self.vel, self.rot_speed)
            self.vel.scale_to_length(min(self.vel.length(), self.speed*dt*1000))
            self.charging = True
        else:
            self.charging = False

        self.angle = self.vel.as_polar()[1]
        self.pos += self.vel
    
    def rot_center(self, image):
        angle = self.angle
        image = pygame.transform.rotate(image, round(-angle-90, 1))
        self.rect = image.get_rect(center = self.rect.center)
        return image
        # self.mask = pygame.mask.from_surface(self.image, True)

    def kill(self):
        super().kill()

class DemonBat(Bat):
    def set_stats(self):
        self.health = 8
        self.speed = 20
        self.speed_norm = 20
        self.speed_zoom= 20 + random.random()*20
        self.angle = 0
        self.rot_speed = 0.01
        self.rot_speed_norm = 0.02
        self.rot_speed_zoom = 0.03
        self.charge_range = 800
        self.attack_range = 40
        self.boom_range = 50
        self.damage = 8

    def create_body(self):
        self.animations = Animator({
            "flying": pygame.image.load(asset("enemies/bat/demon_bat_flying.png")), 
        }, 60, mode = "flying", transforms = [self.rot_center])
        self.image = self.animations.getFirstFrame()
        self.rect = pygame.Rect(self.objT.x, self.objT.y, *self.image.get_size())

        self.particles = fx.PhantomTrail(self.game)

    def update(self):
        if util.distance(tuple(self.pos), self.game.player.rect.center) <  self.charge_range/2:
            self.rot_speed = self.rot_speed_zoom
            self.speed = self.speed_zoom
        else:

            self.rot_speed = self.rot_speed_norm
            self.speed = self.speed_norm
        super().update()
        self.particles.update(self.image, self.rect.copy())

    def kill(self):
        super().kill()
        self.particles.kill()

