import pygame, pymunk, random
import os
from src.stgs import *

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

def print_stats(func):
    if DEBUG:
        output = "stats.txt"
        if os.path.isfile(output):
            os.remove(output)
        class temp:
            pass
        cache = [] 
        def func_new(arg):
            if not arg.__class__.__name__  in cache:
                func(temp)
                with open(output, "+a") as file:
                    file.write("-----" + arg.__class__.__name__ + "-----\n")
                    for k,v in temp.__dict__.items():
                        if k[0:1] != "_":
                            file.write("* " + str(k) + ": " + str(v) +"\n")
                    file.write("\n\n")
                cache.append(arg.__class__.__name__)
            func(arg)
        return func_new
    else:
        return func

