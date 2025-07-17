from src.stgs import *
from src import util

class ClassName(util.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.layer1
        super().__init__(self.groups)
        
        self.dump(kwargs, objT.properties) 
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
