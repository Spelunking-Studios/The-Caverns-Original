import pygame
import colors as cols
from stgs import *
from menu import *

pygame.font.init()
class Text:
    def __init__(self, fNum, text, color, aalias=True, pos=(0, 0), multiline=False, size=(900, 600), bgColor=(0, 0, 0, 0)):
        if multiline:
            ## This code is thanks to https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame 
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            self.image.fill(bgColor)
            font = fonts[fNum]
            words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
            space = font.size(' ')[0]  # The width of a space.
            max_width, max_height = size
            x, y = 0, 0
            for line in words:
                for word in line:
                    if word  != '':
                        if word[0:3] == "RGB":
                            wordsplit = word[4:].split(')')
                            word_color = tuple([int(x) for x in wordsplit[0].split(',')])
                            word = wordsplit[1]
                        else:
                            word_color = color
                        word_surface = font.render(word, aalias, word_color)
                        word_width, word_height = word_surface.get_size()
                        if x + word_width >= max_width:
                            x = 0  # Reset the x.
                            y += word_height  # Start on new row.
                        self.image.blit(word_surface, (x, y))
                        x += word_width + space
                x = 0 # Reset the x.
                y += word_height  # Start on new row.
            
        else: 
            self.image = fonts[fNum].render(text, aalias, color)
        self.pos = pygame.Vector2(pos)
        
        self.rect = (self.pos.x, self.pos.y, size[0], size[1])
        self.image = self.image.convert_alpha()
    
    def __str__(self):
        return self.rend

def transparentRect(size, alpha, color=(0, 0, 0)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((color[0], color[1], color[2], alpha))
    return surf.convert_alpha() 

class pauseOverlay(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.overlayer)
        self.components = pygame.sprite.Group()
        self.text = []
        self.active = False
        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.Surface((winWidth, winHeight), pygame.SRCALPHA).convert_alpha()
        self.loadComponents()
        self.render()

    def loadComponents(self):
        for comp in self.components:
            comp.kill()
            
        self.audioSlider1 = settingSlider(self.game, (100, 350), addGroups = [self.components])
        self.audioSlider2 = settingSlider(self.game, (100, 500), addGroups = [self.components])
        self.audioSlider1.image.set_colorkey((0,0,0))
        self.audioSlider2.image.set_colorkey((0,0,0))
        self.fpsButton = button(self.game, (800, 250), text = 'Toggle FPS', onClick = lambda:self.game.toggleFps() ,groups = [self.components], center = True, colors=(colors.yellow, colors.white))
        self.aaliasButton = button(self.game, (800, 330), text = 'Toggle Anti - Aliasing', onClick = lambda:self.game.toggleAalias() ,groups = [self.components], center = True, colors=(colors.yellow, colors.white))
        button(self.game, (350, 550), groups = [self.components], text = "Return to menu", onClick=self.game.endgame, center = True, colors = (colors.yellow, colors.white))
    
        self.text = [
            Text('5', 'Paused', cols.orangeRed, self.game.antialiasing, (self.rect.width/2.4, 10)),
            Text('1', 'Audio Control', cols.orangeRed, self.game.antialiasing, (75, 250)),
            Text('6', 'Music Volume', cols.orangeRed, self.game.antialiasing, (75, 325)),
            Text('6', 'Fx Volume', cols.orangeRed, self.game.antialiasing, (75, 475))
        ]

        self.audioSlider1.setRatio(self.game.mixer.musicVolume)
        self.audioSlider2.setRatio(self.game.mixer.fxVolume)
        
    def applyComponents(self):
        self.game.mixer.setMusicVolume(self.audioSlider1.get_ratio())
        self.game.mixer.setFxVolume(self.audioSlider2.get_ratio())

    def activate(self):
        self.active = True
        self.audioSlider1.setRatio(self.game.mixer.musicVolume)
        self.audioSlider2.setRatio(self.game.mixer.fxVolume)

    def deactivate(self):
        self.active = False

    def update(self):
        if self.active:
            self.render()
            self.components.update()
            self.applyComponents()
    
    def render(self):
        self.image.fill((0,0,0,190)) #self.transparent)
        for comp in self.components:
            self.image.blit(comp.image, comp.rect)
        for text in self.text:
            self.image.blit(text.image, text.pos)

class mapOverlay(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.overlayer)
        self.components = pygame.sprite.Group()
        self.text = []
        self.active = False
        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.Surface((winWidth, winHeight), pygame.SRCALPHA).convert()
        self.loadComponents()
        self.render()

    def loadComponents(self):
        for comp in self.components:
            comp.kill()
            
        self.mapImage = pygame.image.load(asset('gameMap.png'))
        self.mapImage = pygame.transform.scale(self.mapImage, (int(winWidth), int(winHeight))).convert()

    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False

    def update(self):
        now = pygame.time.get_ticks()
        if self.active:
            self.render()
            self.components.update()
            if checkKey("map") and now - self.game.lastPause >= 180:
                self.deactivate()
                self.game.unPause()
                self.game.lastPause = now
        else:
            if checkKey("map") and now - self.game.lastPause >= 180:
                self.activate()
                self.game.pause = True
                self.game.lastPause = now
    
    def render(self):
        self.image.fill((0,0,0,190)) #self.transparent)
        self.image.blit(self.mapImage, (0, 0))
        # for comp in self.components:
        #     self.image.blit(comp.image, comp.rect)
        # for text in self.text:
        #     self.image.blit(text.image, text.pos)      

class dialogueOverlay(pygame.sprite.Sprite):
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
        self.baseImage = pygame.Surface((winWidth, self.height*self.tileSize), pygame.SRCALPHA)
        #rendText = Text(1, self.text, self.textColor, self.aalias, (self.tileSize, self.tileSize), True)
        #self.baseImage.blit(rendText.image, rendText.pos)
        self.tWidth = int(self.baseImage.get_width()/self.tileSize)
        self.tHeight = int(self.baseImage.get_height()/self.tileSize)

        for x in range(0, self.tWidth-1):
            for y in range(0, self.tHeight-1):
                self.baseImage.blit(self.borderPalette, (x*self.tileSize, y*self.tileSize), (self.tileSize, self.tileSize, self.tileSize, self.tileSize))

        for x in range(1, self.tWidth-1): # Renders top, bottom tiles
            self.baseImage.blit(self.borderPalette, (x*self.tileSize, 0), (self.tileSize, 0, self.tileSize, self.tileSize))
            self.baseImage.blit(self.borderPalette, (x*self.tileSize, self.baseImage.get_height()-self.tileSize), (self.tileSize, self.tileSize*2, self.tileSize, self.tileSize))
        
        for y in range(1, self.tHeight-1): # Renders left, right tiles
            self.baseImage.blit(self.borderPalette, (0, y*self.tileSize), (0, self.tileSize, self.tileSize, self.tileSize))
            self.baseImage.blit(self.borderPalette, (self.baseImage.get_width()-self.tileSize, y*self.tileSize), (self.tileSize*2, self.tileSize, self.tileSize, self.tileSize))
                    
        self.baseImage.blit(self.borderPalette, (0, 0), (0, 0, self.tileSize, self.tileSize))
        self.baseImage.blit(self.borderPalette, (self.baseImage.get_width()-self.tileSize, 0), (self.tileSize*2, 0, self.tileSize, self.tileSize))
        self.baseImage.blit(self.borderPalette, (0, self.baseImage.get_height()-self.tileSize), (0, self.tileSize*2, self.tileSize, self.tileSize))
        self.baseImage.blit(self.borderPalette, (self.baseImage.get_width()-self.tileSize, self.baseImage.get_height()-self.tileSize), (self.tileSize*2, self.tileSize*2, self.tileSize, self.tileSize))

        self.rendText = dText('1', self.text, colors.white, True, (self.tileSize, self.tileSize), (int(self.image.get_width()-self.tileSize*2), int(self.image.get_height()-self.tileSize*2)))
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