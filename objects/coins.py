import random

import fx
import pygame
from animations import *
from stgs import *

from .consumable import consumable

class coinBit(consumable):
    def __init__(self, game, objT):
        super().__init__(game, objT, image = pygame.image.load(asset('objects/bitCoin.png')), value = 5)