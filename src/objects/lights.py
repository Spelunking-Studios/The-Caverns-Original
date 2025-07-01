from src import util
import pygame
from src.animations import *
from src.stgs import *


class LightSource(util.Sprite):
    source_img = pygame.image.load(asset("objects/light2.png"))
    cache = {}

    # objT may also be a Rect()

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.groups.lightSources
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.default_size = False
        if not isinstance(objT, pygame.Rect):
            self.dump(objT.properties)
            self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        else:
            self.rect = objT

        self.pos = pygame.Vector2((self.rect.x, self.rect.y))
        self.dump(kwargs)        

        if self.default_size:
            self.image = self.source_img.copy().convert_alpha()
        else:
            self.resize_wh(self.rect.w)
        self.rect = self.image.get_rect(center=self.rect.center)

    def resize_scale(self, new_scale):
        w, h = self.rect.size
        self.image = pygame.transform.scale(self.source_img, (int(w*new_scale), int(h*new_scale)))

    def resize_wh(self, w, h=False):
        w, h = int(w), int(w)
        if not w in self.cache:
            self.cache[w] = pygame.transform.scale(self.source_img, (w, h))
        self.image = self.cache[w]

class LightEffect(LightSource):
    '''A light source that dies out after a certain amount of time
    '''
    def __init__(self, game, rect, **kwargs):
        self.lifespan = 900
        self.scale = 1
        self.init = now()
        super().__init__(game, rect, img=asset("objects/light1.png"), **kwargs)
    
        # if self.scale != 1:
        #     self.resize(new_scale)

    def update(self):
        if now()-self.init >= self.lifespan:
            self.kill()


