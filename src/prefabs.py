import pygame
from src.menu import *
from src.items import *
from src.objects import *
from src.util import colors, Sprite

class RedButton(Button):
    def __init__(self, game, pos, text, func):
        super().__init__(game,
                         pos,
                         groups=[game.pSprites, game.overlayer],
                         text=text,
                         onClick=func,
                         instaKill=True,
                         center=True,
                         active=True,
                         colors=(colors.orangeRed, colors.white))
