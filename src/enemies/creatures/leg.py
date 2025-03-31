import pygame
import math
import numpy as np
from pygame import Vector2 as Vec
from src.stgs import *
from src.util.fabrik import fabrik
from .chain import SimpleChain

class Leg:
    """A spider leg driven by inverse kinematics
    """

    def __init__(self, length):
        self.length = length 
        self.speed = 2
        self.range = 22
        self.start = Vec(0, 0)
        self.target = Vec(0, 0)
        self.focus = Vec(150, -200)
        self.return_mode = False
        self.phase = 0
        self.reset = True
        self.color = (255,255,255)
        self.built = False
        self.points = [Vec(0, 0) for i in range(3)]

    def build(self, start):
        print(self.length)
        self.start = start
        length = self.length
        segment = Vec(length, 0)

        self.points = [start, start + segment.rotate(np.sign(length)*45), start + (math.sqrt(2)*length, 0)]

    def update(self, start, target, direction, phase = 0, bend=1):
        if not self.built:
            self.build(start)
            self.built = True
        elif self.phase > phase:
            for p in self.points:
                p += start-self.start
            self.start = start

            fabrik(self.points, self.target)
            self.fix_bend()

            if self.return_mode:
                self.target += (target-self.target).normalize()*self.speed 
                if self.target.distance_to(target) < 1:
                    self.return_mode = False
            elif self.target.distance_to(target) > self.range:
                self.return_mode = True 
            pass
        else:
            self.target = target
            for p in self.points:
                p += start-self.start
            self.start = start
        self.phase += 1
    
    def fix_bend(self):
        dir = (self.points[0] - self.points[2]).rotate(90)
        if np.sign(dir.dot(self.points[0]-self.points[1])) != np.sign(self.length):
            p = self.points[1] - self.points[0]
            v = (self.points[0] - self.points[2]).normalize()
            self.points[1] = 2*(p.dot(v)/(v.dot(v)))*v - p + self.points[0]

    def draw(self, surf, transform=lambda x: x):
        for i in range(1, len(self.points)):
            prev = pygame.Rect(*self.points[i-1], 1, 1)
            cur = pygame.Rect(*self.points[i], 1, 1)
            pygame.draw.aaline(surf, self.color, transform(prev).topleft, transform(cur).topleft, 3)
