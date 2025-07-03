from src.menu import *
from src.items import *
from src.objects import *
from src.util import colors

class RedButton(Button):
    def __init__(self, game, pos, text, func):

        super().__init__(game,
                         (400, 400),
                         groups=[game.pSprites, game.overlayer],
                         text="Continue",
                         onClick=func,
                         instaKill=True,
                         center=True,
                         colors=(colors.orangeRed, colors.white))
