from src import util
import pygame
from src.animations import *
from src.stgs import *
import pygame_light2d as pl2d



class LightSource(util.Sprite):
    # objT may also be a Rect()

    def __init__(self, game, objT, **kwargs):
        self.groups = game.sprites, game.groups.lightSources
        self.img_choice = 0
        self.game = game
        self.radius = 450
        self.power = 0.8
        self.color = (255, 255, 255)

        self.dump(kwargs)
        super().__init__(self.groups)
        if not isinstance(objT, pygame.Rect):
            self.dump(objT.properties)
            self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        else:
            self.rect = objT

        self.point_light = pl2d.PointLight(self.rect.center, power=self.power, radius=self.radius)
        self.point_light.set_color(*self.color)
        self.game.display.add_light(self.point_light)
        self.pos = pygame.Vector2(self.rect.center)

    def resize_wh(self, w, h=False):
        # self.light.size blah blah 
        pass

    def update(self):
        self.point_light.position = self.game.cam.applyTuple(self.pos)
        self.point_light.power = self.power 

    def kill(self):
        self.game.display.remove_light(self.point_light)
        super().kill()

class LightEffect(LightSource):
    '''A light source that dies out after a certain amount of time
    '''
    def __init__(self, game, rect, **kwargs):
        self.lifespan = 900
        self.scale = 1
        self.init = now()
        super().__init__(game, rect, **kwargs)
    

    def update(self):
        super().update()
        if now()-self.init >= self.lifespan:
            self.kill()



