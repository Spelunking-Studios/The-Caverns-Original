import pygame
from stgs import winWidth, winHeight, checkKey, asset, fonts
from menu import createFrame
import colors

class DialogueOverlay(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.overlayer)
        self.components = pygame.sprite.Group()
        self.text = []
        self.active = True
        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.Surface((winWidth, winHeight), pygame.SRCALPHA).convert_alpha()
        self.loadComponents()
        self.render()
        self.lastInteract = pygame.time.get_ticks()

    def loadComponents(self):
        self.components = pygame.sprite.Group()

    def activate(self):
        self.active = True
        self.lastInteract = pygame.time.get_ticks()
        self.game.pause = True
        self.game.lastPause = pygame.time.get_ticks()
        
    def deactivate(self):
        self.active = False
        self.lastInteract = pygame.time.get_ticks()
        self.game.pause = False
        self.game.lastPause = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        compLen = len(self.components.sprites())
        if self.active:
            self.render()
            if compLen == 0:
                self.deactivate()
            else:
                self.components.update()
                if checkKey("interact") and now-self.lastInteract > 200:
                    lastSpr = self.components.sprites()[compLen-1]
                    if lastSpr.finished:
                        for comp in self.components:
                            comp.kill()    
                        self.deactivate()
        else:
            pass
    
    def render(self):
        for comp in self.components:
            self.image.blit(comp.image, comp.rect)
    
    def dialogue(self, npc):
        self.activate()
        self.components.add(Dialogue(self.game, npc.text))

class Dialogue(pygame.sprite.Sprite):
    def __init__(self, game, text, **kwargs):
        self.groups = game.sprites, game.overlayer
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.height = 8
        self.tileSize = 32
        self.text = text
        self.rect = pygame.Rect(0, winHeight-self.height*self.tileSize, winWidth, self.height*self.tileSize)
        self.textColor = colors.white
        self.lastInteract = pygame.time.get_ticks()
        self.aalias = True
        self.borderPalette = pygame.image.load(asset('objects/dPallette2.png'))
        if self.borderPalette.get_width()/self.tileSize < 3 or self.borderPalette.get_height()/self.tileSize < 3 :
            print("Check your pallette size. It is currently invalid for the  set tile size.")
        self.render()
        self.finished = False

    def render(self):
        self.image = pygame.Surface((winWidth, self.height*self.tileSize), pygame.SRCALPHA)
        self.baseImage = createFrame(winWidth/self.tileSize, self.height)
        self.rendText = dText('title1', self.text, colors.white, True, (self.tileSize, self.tileSize), (int(self.image.get_width()-self.tileSize*2), int(self.image.get_height()-self.tileSize*2)))
        self.baseImage.convert_alpha()
        self.image.blit(self.baseImage, (0, 0))
        self.renderText()
        self.image.convert_alpha()
    
    def renderText(self):
        self.image.blit(self.rendText.getCurrent(), self.rendText.pos)

    def refresh(self):
        self.image = self.baseImage
        self.renderText()

    def update(self):
        now = pygame.time.get_ticks()
        if len(self.rendText.images) > 1:
            if checkKey("interact") and now-self.lastInteract > 200:
                if self.rendText.index+1 >= len(self.rendText.images):
                    self.finished = True
                else:
                    self.rendText.index += 1
                self.refresh()
                self.lastInteract = now
        else:
            self.finished = True

        
            

class dText:
    def __init__(self, fNum, text, color, aalias=True, pos=(0, 0), size=(900, 600), bgColor=(0, 0, 0, 0)):
        ## This code is thanks to https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame.
        self.render(fNum, text, color, aalias, pos, size, bgColor)
        self.pos = pygame.Vector2(pos)
        
        self.rect = (self.pos.x, self.pos.y, size[0], size[1])
        for img in self.images:
            img.convert_alpha()

    def getCurrent(self):
        return self.images[self.index]

    def render(self, fNum, text, color, aalias=True, pos=(0, 0), size=(900, 600), bgColor=(0, 0, 0, 0)):
        self.images = [pygame.Surface(size, pygame.SRCALPHA)] 
        self.index = 0
        self.getCurrent().fill(bgColor)

        font = fonts[fNum]
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = size
        x, y = 0, 0
        for line in words:
            for word in line:
                if word  != '':
                    word_surface = font.render(word, aalias, color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = 0  # Reset the x.
                        y += word_height  # Start on new row.
                    if y > max_height-word_height:
                        x, y = 0, 0
                        self.getCurrent().convert_alpha()
                        self.index += 1
                        self.images.append(pygame.Surface(size, pygame.SRCALPHA))
                    else:
                        self.getCurrent().blit(word_surface, (x, y))
                        x += word_width + space
            
        self.index = 0

    
    def __str__(self):
        return self.image