import pygame
from pygame import Vector2 as Vec

from src.animations import Animator
from src.stgs import *
from src import util
from src import fx
from .enemy import SimpleEnemy

from src.util import print_stats

class BoomBug(SimpleEnemy):
    """A very small and quick bug that catches you by 
    suprise and then Boom
    """

    challenge_rating = 1

    def __init__(self, game, objT):
        super().__init__(game, objT)

        self.set_stats() 
        self.create_body()
        self.create_physics(500, 5, self.movement, (objT.x, objT.y))
    
    @print_stats
    def set_stats(self):
        self.health = 8
        self.speed = 800
        self.angle = 0
        self.rot_speed = 0.05
        self.charge_range = 800
        self.boom_range = 50
        self.boom_damage = 20
        self.damage = self.boom_damage
        self.boom_power = 200000

    def create_body(self):
        self.animations = Animator({
            "walking": pygame.image.load(asset("enemies/boom bug/boombug.png")), 
            "boom": pygame.image.load(asset("enemies/boom bug/boombug_boom.png"))
        }, 60, mode = "walking", transforms = [self.rot_center])
        self.animations.set_callback("boom", self.boom)
        self.image = self.animations.getFirstFrame()
        self.rect = pygame.Rect(self.objT.x, self.objT.y, *self.image.get_size())
        self.particles = fx.SlowGlowParticles(self.game, color = util.wheat_gold, speed = 0.5)

    def update(self):
        super().update()
        pos = self.body.position
        self.rect.center = pos
        self.particles.position = pos
        if util.distance(self.rect.center, self.game.player.rect.center) <= self.boom_range:
            self.animations.set_mode("boom")

        self.animations.update()
        self.image = self.animations.get_image()

    def boom(self):

        super().deal_damage()

        #calculate knockback
        diff = Vec(self.game.player.body.position) - Vec(self.body.position) 
        # self.debug_render = [head.position, player.body.position]
        diff.scale_to_length(self.boom_power)
        self.game.player.body.apply_impulse_at_local_point(tuple(diff), (0, 0))

        #play boom sound

        #shockwave

        self.kill()

    def movement(self, body, gravity, damping, dt):
        old_vel = Vec(body.velocity)
        pos = body.position
        if util.distance(pos, self.game.player.rect.center) <  self.charge_range:
            vel = (self.game.player.rect.center - Vec(pos)).normalize()*self.speed
            vel = old_vel.lerp(vel, self.rot_speed)
            vel.scale_to_length(min(vel.length(), self.speed*dt*1000))
            self.angle = vel.as_polar()[1]
            body.velocity = tuple(vel)
    
    def rot_center(self, image):
        angle = self.angle
        image = pygame.transform.rotate(image, round(-angle-90, 1))
        self.rect = image.get_rect(center = self.rect.center)
        return image
        # self.mask = pygame.mask.from_surface(self.image, True)

    def kill(self):
        super().kill()
        self.particles.kill()
