from menu import *
from items import *
from objects import *

class RedButton(Button):
    def __init__(self, game, pos, text, func):

        super().__init__(game,
                         (400, 400), 
                         groups = [game.pSprites, game.overlayer], 
                         text = "Continue", 
                         onClick = func, 
                         instaKill = True, 
                         center = True, 
                         colors = (colors.orangeRed, colors.white))

