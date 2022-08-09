import pygame
from .enemy import Enemy
import stgs

class Rat(Enemy):
    """A rat enemy"""
    def __init__(self, room, objT):
        Enemy.__init__(self, room, objT)
