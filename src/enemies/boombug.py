import pygame
from pygame import Vector2 as Vec

from src.animations import Animator
from src.stgs import *
from src import util
from .enemy import SimpleEnemy


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

    def set_stats(self):
        self.health = 20
        self.speed = 3000
        self.rot_speed = 2
        self.attack_range = 500

    def create_body(self):
        self.animations = Animator({
            "walking": pygame.image.load(asset("enemies/boombug.png"))
        }, 40, mode = "walking", transforms = [self.rot_center])
        self.image = self.animations.getFirstFrame()
        self.rect = pygame.Rect(0, 0, *self.image.get_size())

    def update(self):
        return super().update()
        self.rect.center = self.body.position

    def movement(self, body, gravity, damping, dt):
        old_vel = Vec(body.velocity)
        pos = body.position
        if util.distance(pos, self.game.player.rect.center) > self.attack_range:
            vel = (self.game.player.rect.center - Vec(pos)).normalize()*self.speed
            vel = old_vel.lerp(vel, self.rot_speed)
            vel.scale_to_length(min(vel.length(), self.speed*dt*1000))
            self.angle = vel.as_polar()[1]
            body.velocity = tuple(vel)
    
    def rot_center(self, angle=False):
        if not angle:
            angle = self.angle
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)
        self.mask = pygame.mask.from_surface(self.image, True)
