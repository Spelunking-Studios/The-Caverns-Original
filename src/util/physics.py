from src.stgs import *
from .sprite import Sprite


class Ball(Sprite):
    """
    Creates a ball like object
    """
    def __init__(self, radius = 10, pos = (20, 20)):
        self.body = pymunk.Body(100, 100)
        self.body.position = pos
        self.shape = pymunk.Circle(body, radius, (0, 0))
        self.shape.friction = 0.5
        self.shape.collision_type = COLLTYPE_BALL

    def objects(self):
        return self.body, self.shape
        
class Chain(Sprite):
    """
    Creates a chain of balls. Acts as a controller and accepts
    an optional velocity function for the first chain link
    """
    def __init__(self, length, radius, link_distance, controller=None):
        self.length = length
        self.ball_radius = radius
        self.link_distance = link_distance
        self.chain_angles = []
        self.controller = controller

        self.create()

    def create(self):
        self.balls = []
        for i in range(self.length):
            ball = Ball(self.ball_radius ,(i*self.link_distance, i*self.link_distance))
            if self.controller and i == 0:
                ball.body.velocity_func = self.owner.head_movement
            self.balls.append(ball)
            self.game.space.add(ball.objects)

        self.joints = []
        for i in range(self.length-1):
            joint = pymunk.PinJoint(self.bodies[i], self.bodies[i+1], (0,0), (0,0))
            self.joints.append(joint)
            self.space.add(joint)

    def get_points(self):
        return [ball.body.position for ball in self.balls]

    def update(self, dt):
        # Store angles
        points = self.get_points()
        for i in range(1, len(points)):
            delta = points[i] - points[i-1]
            self.chain_angles[i] = delta.as_polar()[1]


