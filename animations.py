import pygame
from stgs import *


class rotAnimation:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    def __init__(self, sprite, imgSheet):
        self.sprite = sprite
        self.framex = 0
        self.delay = 120
        self.scalex, self.scaley = 1,1
        self.imgSheet = Spritesheet(imgSheet)
        self.tileSize = self.imgSheet.height
        self.tileWidth, self.tileHeight = self.tileSize, self.tileSize
        self.lastTick = pygame.time.get_ticks()
        self.imageEffects = pygame.sprite.Group()

    def update(self):
        if pygame.time.get_ticks() - self.lastTick >= self.delay:
            self.framex += self.tileWidth
            self.lastTick = pygame.time.get_ticks()
            if self.framex > int(self.imgSheet.width - self.tileWidth):
                self.framex = 0
        self.sprite.image = self.imgSheet.get_image(self.framex, 0, self.tileWidth, self.tileHeight)
        if not self.scalex == 1 or not self.scaley == 1:
            self.sprite.image = pygame.transform.scale(self.sprite.image, (self.tileWidth*self.scalex, self.tileHeight*self.scaley))
        self.sprite.rotCenter()
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

class playerAnimation:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    def __init__(self, sprite):
        self.sprite = sprite
        self.framex = 0
        self.delay = 120
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
        if not self.scalex == 1 or not self.scaley == 1:
            self.sprite.image = pygame.transform.scale(self.sprite.image, (self.tileSize*self.scalex, self.tileSize*self.scaley))
        self.sprite.rotCenter()
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

class animation:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    ## Full image sheet can contain: 'active', 'tileWidth', 'tileHeight', 'r', 'l', 'idleR', 'idleL','flyR', 'flyL'
    def __init__(self, sprite):
        self.sprite = sprite
        self.loadSheet()
        self.framex = 0
        self.delay = 120
        self.imageEffects = pygame.sprite.Group()
        self.rotation = False
        self.scalex, self.scaley = 1,1
        self.dir = 'idleR'
        self.lastTick = pygame.time.get_ticks()

    def loadSheet(self): #Very long tedious function
        self.imgSheet = self.sprite.imgSheet
        for k, v in self.imgSheet.items():
            if not k == 'active' and not k == 'tileWidth' and not k == 'tileHeight':
                self.imgSheet[k] = Spritesheet(v)
        
        self.tileWidth = self.imgSheet['tileWidth']
        self.hasIdle = True 
        self.hasFly = True

        try:
            self.imgSheet['l']
        except:
            self.imgSheet['l'] = Spritesheet(pygame.transform.flip(self.imgSheet['r'].image, True, False), True)
        try:
            self.imgSheet['idleL']
        except:
            try:
                self.imgSheet['idleL'] = Spritesheet(pygame.transform.flip(self.imgSheet['idleR'].image, True, False), True)
            except:
                self.hasIdle = False
        try:
            self.imgSheet['flyL']
        except:
            try:
                self.imgSheet['flyL'] = Spritesheet(pygame.transform.flip(self.imgSheet['flyR'].image, True, False), True)
            except:
                self.hasFly = False
        try:
            self.tileHeight = self.imgSheet['tileHeight']
        except:
            self.tileHeight = self.tileWidth
        
    def update(self):
        self.getStrDir()

        if pygame.time.get_ticks() - self.lastTick >= self.delay:
            self.framex += self.tileWidth
            self.lastTick = pygame.time.get_ticks()
            if self.framex > int(self.imgSheet[self.dir].width - self.tileWidth):
                self.framex = 0
        try:
            if self.sprite.imgSheet['active']:
                if self.rotation:
                        self.sprite.image = pygame.transform.scale(self.imgSheet[self.dir].get_image(self.framex, 0, self.tileWidth, self.tileHeight), (self.tileWidth*self.scalex, self.tileHeight*self.scaley))
                        
                        self.sprite.rotCenter(self.sprite.angle)
                else:
                    self.sprite.image = self.imgSheet[self.dir].get_image(self.framex, 0, self.tileWidth, self.tileHeight)
                    if not self.scalex == 1 or not self.scaley == 1:
                        self.sprite.image = pygame.transform.scale(self.sprite.image, (self.tileWidth*self.scalex, self.tileHeight*self.scaley))
                
                self.applyFx()
        except KeyError:  ## This is deprecated
            self.sprite.image = self.imgSheet[self.dir].get_image(self.framex, 0, self.tileWidth, self.tileHeight)
            self.sprite.image.set_colorkey((0,0,0))
            

    def getStrDir(self):
        ### Get the last specific direction
        
        lastDir = ''
        fullLastDir = self.dir
        if len(self.dir) == 1:
            lastDir = self.dir
        elif self.dir[0:4] == 'idle':
            lastDir = self.dir[4]
        else:
            lastDir = self.dir[3]

        if self.hasFly:
            if self.sprite.ground:
                if self.sprite.dir.x > 0:
                    self.dir = 'r'
                elif self.sprite.dir.x < 0:
                    self.dir = 'l'
                elif self.hasIdle:
                    self.dir = 'idle' + lastDir.capitalize()
                else:
                    self.dir = lastDir.lower()
            else:
                if self.sprite.dir.x > 0:
                    self.dir = 'flyR'
                elif self.sprite.dir.x < 0:
                    self.dir = 'flyL'
                else:
                    self.dir = 'fly' + lastDir.capitalize()
        else:
            if self.sprite.dir.x > 0:
                self.dir = 'r'
            elif self.sprite.dir.x < 0:
                self.dir = 'l'
            elif self.hasIdle:
                self.dir = 'idle' + lastDir.capitalize()
            else:
                self.dir = lastDir.lower()
        
        if not self.dir == fullLastDir:
            self.framex = 0
    
    def applyFx(self):
        for fx in self.imageEffects:
            fx.update(self.sprite.image)
    
    def fx(self, fx):
        self.imageEffects.add(fx)

    def scale(self, x, y=None):
        if y==None:
            self.scalex, self.scaley = x,x
        else:
            self.scalex, self.scaley = x,y

class hurtFx(pygame.sprite.Sprite):
    def __init__(self, duration = 300):
        pygame.sprite.Sprite.__init__(self)
        self.start = pygame.time.get_ticks()
        self.duration = duration

    def update(self, image):
        time = pygame.time.get_ticks() - self.start
        if time < self.duration:
            darkness = min(255, max(0, round(255 * (time/self.duration))))
            image.fill((255, darkness, darkness), special_flags = pygame.BLEND_MULT)
        else:
            self.kill()

class animation2:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    def __init__(self, sprite):
        self.sprite = sprite
        self.loadSheet()
        self.framex = 0
        self.delay = 120
        self.rotation = False
        self.scalex, self.scaley = 1,1
        self.dir = 'idleR'
        self.lastTick = pygame.time.get_ticks()
        self.imageEffects = pygame.sprite.Group()

    def loadSheet(self):
        self.imgSheet = self.sprite.imgSheet
        for k, v in self.imgSheet.items():
            if not k == 'active' and not k == 'tileWidth' and not k == 'tileHeight':
                self.imgSheet[k] = Spritesheet(v)
        
        self.tileWidth = self.imgSheet['tileWidth']
        self.hasIdle = True 
        self.hasFly = True

        try:
            self.imgSheet['l']
        except:
            self.imgSheet['l'] = Spritesheet(pygame.transform.flip(self.imgSheet['r'].image, True, False), True)
        try:
            self.imgSheet['u']
        except:
            self.imgSheet['u'] = Spritesheet(pygame.transform.flip(self.imgSheet['d'].image, False, True), True)
        try:
            self.tileHeight = self.imgSheet['tileHeight']
        except:
            self.tileHeight = self.tileWidth
        
    def update(self):
        self.getStrDir()

        if pygame.time.get_ticks() - self.lastTick >= self.delay:
            self.framex += self.tileWidth
            self.lastTick = pygame.time.get_ticks()
            if self.framex > int(self.imgSheet[self.dir].width - self.tileWidth):
                self.framex = 0
        self.sprite.image = self.imgSheet[self.dir].get_image(self.framex, 0, self.tileWidth, self.tileHeight)
        if not self.scalex == 1 or not self.scaley == 1:
            self.sprite.image = pygame.transform.scale(self.sprite.image, (self.tileWidth*self.scalex, self.tileHeight*self.scaley))
        self.applyFx()
            

    def getStrDir(self):
        ### Get the last specific direction 
        lastDir = self.dir
        if self.sprite.dir.x > 0:
            self.dir = 'r'
        elif self.sprite.dir.x < 0:
            self.dir = 'l'
        elif self.sprite.dir.y > 0:
            self.dir = 'd'
        elif self.sprite.dir.y < 0:
            self.dir = 'u'
        else:
            self.dir = 'r'

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