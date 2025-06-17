import pygame, pymunk, random

from .camera import Cam
from .display import Display
from .fabrik import fabrik
from .grouper import Grouper
from .collisions import Handler
from .math import distance, distance_squared
from .sprite import Sprite
from .colors import *
from .spritesheet import Spritesheet
from .physics import Chain, Ball


class ObjT:
    def __init__(self, **kwargs):
        self.x, self.y = 0, 0
        self.width, self.height = 20, 20
        self.id = random.random()

        for k,v in kwargs.items():
            self.__dict__[k] = v

        self.properties = self.__dict__
