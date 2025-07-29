from src.stgs import *
from src import util
from .lights import LightSource

class Consumable(util.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.layer1, game.groups.interactable
        super().__init__(self.groups)
        
        self.dump(kwargs, objT.properties) 
        self.lID = objT.id
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

    def interact(self):
        self.kill()

class Fungus(Consumable):
    image = pygame.image.load(asset("objects/fungus.png"))
    def __init__(self, game, objT, **kwargs):
        super().__init__(game, objT, **kwargs)
        self.rect.size = self.image.get_size()

        self.light = LightSource(game, self.rect, default_size=True)
        self.light.rect.center = self.rect.center

    def interact(self):
        self.game.player.change_health(10)
        super().interact()

    def kill(self):
        super().kill()
        self.light.kill()

