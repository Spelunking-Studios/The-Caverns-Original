from animations import *
from stgs import *
import util

class ClassName(util.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.dump(kwargs, objT.properties) 
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
