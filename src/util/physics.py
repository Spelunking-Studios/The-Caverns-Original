import pygame, pymunk
from pygame import Vector2 as Vec

from src.stgs import *
from .sprite import Sprite


class Ball(Sprite):
    """
    Creates a ball like object
    """
    def __init__(self, radius = 10, pos = (20, 20), mass=100, moment=100):
        super()
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.friction = 0.5
        self.shape.collision_type = 3

    def objects(self):
        return self.body, self.shape

class Chain(Sprite):
    """
    Creates a chain of balls. Acts as a controller and accepts
    an optional velocity function for the first chain link
    """
    def __init__(self, game, length, pos, radius, link_distance, controller=None, **kwargs):
        self.game = game
        self.length = length
        self.pos = pos
        self.ball_radius = radius
        self.link_distance = link_distance
        self.chain_angles = [0 for i in range(self.length)]
        self.controller = controller
        self.ball_weight = 300

        self.dump(kwargs)

        self.create()

    def create(self):
        x, y = self.pos
        self.balls = []
        for i in range(self.length):
            ball = Ball(self.ball_radius ,(x + i*self.link_distance, y + i*self.link_distance), self.ball_weight)
            if self.controller and i == 0:
                ball.body.velocity_func = self.controller
            self.balls.append(ball)
            self.game.space.add(*ball.objects())

        self.joints = []
        for i in range(self.length-1):
            joint = pymunk.PinJoint(self.balls[i].body, self.balls[i+1].body, (0,0), (0,0))
            self.joints.append(joint)
            self.game.space.add(joint)

    def get_points(self):
        return [ball.body.position for ball in self.balls]

    def update(self):
        # Store angles
        points = self.get_points()
        for i in range(1, len(points)):
            delta = points[i] - points[i-1]
            self.chain_angles[i] = Vec(delta).as_polar()[1]

    def kill(self):
        for b in self.balls:
            self.game.space.remove(*b.objects())
        for j in self.joints:
            self.game.space.remove(j)


