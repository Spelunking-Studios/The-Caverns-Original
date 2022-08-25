from .overlay import Overlay
from .pause import PauseOverlay
from .map import MapOverlay
from .dialogue import DialogueOverlay
from .inventory import InventoryOverlay

import pygame
import colors as cols
from stgs import *
from menu import *

pygame.font.init()

def transparentRect(size, alpha, color=(0, 0, 0)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((color[0], color[1], color[2], alpha))
    return surf.convert_alpha()
