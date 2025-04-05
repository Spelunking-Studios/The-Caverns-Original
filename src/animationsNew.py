import pygame
import util
from src.stgs import *

class Animator:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    cache = {}
    def __init__(self, img_sheet):
        self.framex = 0
        self.delay = 120
        self.scalex, self.scaley = 1,1
        self.img_sheet = img_sheet
        for k,v in self.img_sheet.items():
            self.img_sheet[k] = Spritesheet(v)
        self.mode = 'static'
        self.last_tick = pygame.time.get_ticks()
        self.image_effects = pygame.sprite.Group()
        
        # if type(sprite) in self.cache:
        #     self.img_sheet = self.cache[type(sprite)]
        # else:
        #     print("caching img_sheetchick")
        #     for k, v in self.img_sheet.items():
        #         self.img_sheet[k] = Spritesheet(v)
        #     self.cache[type(sprite)] = self.img_sheet

        self.tile_size = self.img_sheet[self.mode].height
        self.image = pygame.Surface((self.tile_size, self.tile_size))
        self.image.convert_alpha() 

    def getFirstFrame(self):
        return self.img_sheet[self.mode].get_image(0, 0, self.tile_size, self.tile_size)

    def update(self):
        if self.mode == "static":
            self.image = self.img_sheet[self.mode].image
        else:
            if pygame.time.get_ticks() - self.last_tick >= self.delay:
                self.framex += self.tile_size
                self.last_tick = pygame.time.get_ticks()
                if self.framex > int(self.img_sheet[self.mode].width - self.tile_size):
                    self.framex = 0
            self.image = self.img_sheet[self.mode].get_image(self.framex, 0, self.tile_size, self.tile_size)
            if not self.scalex == 1 and not self.scaley == 1:
                self.image = pygame.transform.scale(self.sprite.image, (self.tile_size*self.scalex, self.tile_size*self.scaley))
        self.update_fx()

    def scale(self, x, y=None):
            self.scalex, self.scaley = x,y if y else x
        
    def update_fx(self):
        for fx in self.image_effects:
            fx.update()
    
    def fx(self, fx):
        self.image_effects.add(fx)
    
    def set_mode(self, mode="default"):
        if mode in self.img_sheet:
            self.mode = mode
        else:
            print(f"mode {mode} does not exist for this sprite")
        self.tile_size = self.img_sheet[self.mode].height

    def get_image(self):
        img = self.image.copy()
        for fx in self.image_effects:
            fx.apply(img)
        return img

class MultiAnimator:
    def __init__(self, img_sheets):
        pass


class HurtFx(util.Sprite):
    def __init__(self, duration = 300):
        super().__init__()
        self.start = now()
        self.duration = duration

    def update(self):
        time = now() - self.start
        if time > self.duration:
            self.kill()

    def apply(self, image):
        time = now() - self.start
        darkness = min(255, max(0, round(255 * (time/self.duration))))
        image.fill((255, darkness, darkness), special_flags = pygame.BLEND_MULT)



