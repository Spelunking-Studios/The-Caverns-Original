from src import util
import pygame
from src.stgs import *
from src.util import Spritesheet


class PlayerAnimation:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    def __init__(self, sprite):
        self.sprite = sprite
        self.framex = 0
        self.delay = 50
        self.scalex, self.scaley = 1,1
        self.imgSheet = sprite.imgSheet
        self.mode = "default"
        self.lastTick = pygame.time.get_ticks()
        self.imageEffects = pygame.sprite.Group()
        
        for k, v in self.imgSheet.items():
            self.imgSheet[k] = Spritesheet(v)

        self.tileSize = self.imgSheet[self.mode].height

    def update(self):
        if pygame.time.get_ticks() - self.lastTick >= self.delay:
            self.framex += self.tileSize
            self.lastTick = pygame.time.get_ticks()
            if self.framex > int(self.imgSheet[self.mode].width - self.tileSize):
                self.framex = 0
                if self.mode != "default":
                    self.setMode()
        self.sprite.image = self.imgSheet[self.mode].get_image(self.framex, 0, self.tileSize, self.tileSize)
        if self.scalex != 1 or self.scaley != 1:
            self.sprite.image = pygame.transform.scale(self.sprite.image, (self.tileSize*self.scalex, self.tileSize*self.scaley))
        self.sprite.rotCenter()
        self.applyFx()

    def scale(self, x, y=None):
        if y==None:
            self.scalex, self.scaley = x,x
        else:
            self.scalex, self.scaley = x,y

    def getFirstFrame(self):
        return self.imgSheet[self.mode].get_image(0, 0, self.tileSize, self.tileSize)
        
    def applyFx(self):
        for fx in self.imageEffects:
            fx.update(self.sprite.image)
    
    def fx(self, fx):
        self.imageEffects.add(fx)
    
    def setMode(self, mode="default", delay=60):
        if not self.mode == mode:
            if mode in self.imgSheet:
                self.mode = mode
            else:
                print(f"mode {mode} does not exist for this sprite")
            self.tileSize = self.imgSheet[self.mode].height
            self.framex = 0
            self.delay = delay

class BasicAnimation:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    cache = {}
    def __init__(self, sprite, **kwargs):
        self.sprite = sprite
        self.framex = 0
        self.delay = 120
        self.scalex, self.scaley = 1,1
        self.angle = 0
        self.imgSheet = sprite.imgSheet
        self.mode = 'main'
        self.lastTick = pygame.time.get_ticks()
        self.imageEffects = pygame.sprite.Group()
        
        if type(sprite) in self.cache:
            self.imgSheet = self.cache[type(sprite)]
        else:
            print("caching imgSheet")
            for k, v in self.imgSheet.items():
                self.imgSheet[k] = Spritesheet(v)
            self.cache[type(sprite)] = self.imgSheet

        self.tileSize = self.imgSheet[self.mode].height

        for k, v in kwargs.items():
            self.__dict__[k] = v

    def getFirstFrame(self):
        return self.imgSheet[self.mode].get_image(0, 0, self.tileSize, self.tileSize)

    def update(self):
        if pygame.time.get_ticks() - self.lastTick >= self.delay:
            self.framex += self.tileSize
            self.lastTick = pygame.time.get_ticks()
            if self.framex > int(self.imgSheet[self.mode].width - self.tileSize):
                self.framex = 0
        self.sprite.image = self.imgSheet[self.mode].get_image(self.framex, 0, self.tileSize, self.tileSize)
        if not self.scalex == 1 or not self.scaley == 1:
            self.sprite.image = pygame.transform.scale(self.sprite.image, (self.tileSize*self.scalex, self.tileSize*self.scaley))
        if self.angle != 0:
            self.rotate_center()
        self.applyFx()

    def scale(self, x, y=None):
        if y==None:
            self.scalex, self.scaley = x,x
        else:
            self.scalex, self.scaley = x,y
        
    def applyFx(self):
        for fx in self.imageEffects:
            fx.update(self.sprite.image)
    
    def fx(self, fx):
        self.imageEffects.add(fx)
    
    def setMode(self, mode="default"):
        if mode in self.imgSheet:
            self.mode = mode
        else:
            print(f"mode {mode} does not exist for this sprite")
        self.tileSize = self.imgSheet[self.mode].height

    def rotate_center(self):
        # Rotates sprite about the center
        self.sprite.image = pygame.transform.rotate(self.sprite.image, self.angle)
        self.sprite.rect = self.sprite.image.get_rect(center = self.sprite.rect.center)

# class HurtFx(util.Sprite):
#     def __init__(self, duration = 300):
#         pygame.sprite.Sprite.__init__(self)
#         self.start = pygame.time.get_ticks()
#         self.duration = duration
#
#     def update(self, image, restoreImage = None):
#         time = pygame.time.get_ticks() - self.start
#         if time < self.duration:
#             darkness = min(255, max(0, round(255 * (time/self.duration))))
#             image.fill((255, darkness, darkness), special_flags = pygame.BLEND_MULT)
#         else:
#             # Restore image
#             if restoreImage:
#                 image = restoreImage
#             self.kill()

class Animator:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    cache = {}
    def __init__(self, img_sheet, delay = 120, **kwargs):
        self.framex = 0
        self.delay = delay
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
        # Called when the animation reaches the end
        self.callback = None
        self.hide = False

        for k,v in kwargs.items():
            self.__dict__[k] = v


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
                    if self.callback:
                        self.callback()
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

    def clear_fx(self, fx_type=None):
        if fx_type:
            #add support for removing fx of certain type
            pass
        else:
            self.image_effects.empty() 

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


class GlowFx(util.Sprite):
    def __init__(self, duration = 300, color = None, **kwargs):
        super().__init__()
        self.start = now()
        self.duration = duration
        self.speed = 8
        self.strength = 0.5
        self.color = color

        self.dump(kwargs)

    def update(self):
        time = now() - self.start
        if time > self.duration:
            self.kill()

    def get_color(self):
        time = now() - self.start
        magic = math.sin(time/1000*self.speed)
        if self.color:
            return util.scale_rgb(self.color, (magic+1)*self.strength)
            # return util.light(self.color, (magic-1)*50)
        else:
            darkness = min(255, max(0, round(255 * magic)))
            return (darkness, darkness, darkness)

    def apply(self, image):
        image.fill(self.get_color(), special_flags = pygame.BLEND_ADD)





