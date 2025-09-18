import pygame
from src.menu import *
from src.items import *
from src.objects import *
from src.util import colors, Sprite

class RedButton(Button):
    def __init__(self, game, pos, text, func):
        print("wtf")

        super().__init__(game,
                         pos,
                         groups=[game.pSprites, game.overlayer],
                         text="Continue",
                         onClick=func,
                         instaKill=True,
                         center=True,
                         active=True,
                         colors=(colors.orangeRed, colors.white))

class Event(Sprite):
    def __init__(self, game, objT, **kwargs):
        super().__init__(game, game.sprites)

        self.dump(kwargs, objT.properties)
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

        self.trigger = lambda x: x

    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.trigger(9)

