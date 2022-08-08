import pygame
from pygame.sprite import Group

pygame.init()
import os
import random
import sys

from stgs import loadSave, saveFile
loadSave(saveFile)
from stgs import *
from camera import *
from fx import *
from levels import *
from menu import *
# from objects import *
from overlay import *
from player import *
from sfx import *
import menus
import hud
# from PygameShader.shader import shader_sobel24_fast_inplace, shader_bloom_effect_array24
# from PygameShader.gaussianBlur5x5 import blur5x5_array24_inplace_c



class Grouper:
    '''A class to control and manipulate multiple groups (pygame.group.Group) of game objects that is mainly designed for in code control'''
    def __init__(self):
        """Contains helpful groups for organizing different types of sprites"""
        # Create sprite groups here
        self.enemies = Group()
        self.lightSources = Group()
        self.colliders = Group()
        self.pProjectiles = Group() # Player Projectiles
        self.eProjectiles = Group() # Enemy Projectiles

    def getProximitySprites(self, sprite, proximity=300, *args): 
        '''This function is necessary for framerate saving when attacking with a weapon mesh or is just helpful for getting a smaller list of mobs
        takes: sprite (pygame.sprite.Sprite), proximity (distance in pixels), *args (list of groups you wanna check from or enemies by default)'''

        groups = args if len(args) > 1 else [self.enemies]
        returnList = []
        for g in groups:
            for e in g:
                if pygame.Vector2(e.rect.center).distance_to(pygame.Vector2(sprite.rect.center)) <= proximity:
                    returnList.append(e)
        return returnList
    
    def clearAll(self):
        for g in self.allGroups():
            g.empty()

    def allGroups(self):
        return [self.__dict__[g] for g in self.__dict__ if isinstance(self.__dict__[g], Group)]

#### Game object ####
class Game:
    """Represents an instance of the game"""
    def __init__(self):
        """Initializes the game object
        
        Groups each sprite type to perform targetted tasks
        All sprites go into the sprites group
        Sets up window, font, gravity, and cam
        Loads data for the game levels and the player
        """
        self.layer1 = Group()
        self.layer2 = Group()
        self.fxLayer = Group()
        self.hudLayer = Group()
        self.overlayer = Group()
        self.rendLayers = [self.layer1, self.layer2]
        self.mixer = GameMixer()
        self.mixer.setMusicVolume(musicVolume) # between 0 and 1
        self.mixer.setFxVolume(fxVolume)
        self.antialiasing = aalias

        #pygame.display.set_icon(pygame.image.load(iconPath))
        self.win = pygame.display.set_mode((winWidth, winHeight), winFlags)
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(pygame.image.load(iconPath))
        self.win.convert(32, pygame.RLEACCEL) 
        self.lastPause = pygame.time.get_ticks()
        self.lastReset = pygame.time.get_ticks()
        self.lastCamTog = pygame.time.get_ticks()
        self.points = 0
        self.currentFps = 0
        self.showFps = SHOWFPS
        self.joystickDisabled = joystickDisabled
        self.fullScreen = False
        self.clock = pygame.time.Clock()
        self.loadingScreenShownBefore = LOADING_SCREEN_SHOWN_BEFORE
        self.new()

    def new(self):
        self.won = False
        self.points = 0
        self.groups = Grouper()
        self.sprites = Group()
        self.pSprites = Group()
        self.map = GameMap(self)
        self.player = Player(self, asset('player/samplePlayer.png'))
        self.end = False
        self.pause = False
        self.pauseScreen = PauseOverlay(self)
        self.mapScreen = MapOverlay(self)
        self.dialogueScreen = DialogueOverlay(self)
        self.statsInfo = hud.StatHud(self)
        self.updateT = pygame.time.get_ticks()
        self.cam = Cam(self, winWidth, winHeight)
        

    ####  Determines how the run will function ####
    def run(self):
        loadSave("save.p")
        self.menuLoop()
        #self.mixer.playMusic(asset('sounds/track 1.wav'))
        self.mainLoop()
        self.mixer.stop()
        if self.won:
            self.victoryLoop()
        else:
            self.gameOver()

    #### Main game loop ####
    def mainLoop(self):
        while not self.end:
            self.clock.tick(FPS)
            self.refresh()#asset('objects/shocking.jpg'))

            ##Updates Game
            self.runEvents()
            self.update()

    def update(self): 
        self.getFps()
        self.getPause()
        if self.pause:
            self.pSprites.update()
        else:
            self.sprites.update()
            self.checkHits()
        self.overlayer.update()
        self.cam.update()
        
        self.render()

        pygame.display.update()

    def render(self):
        self.win.blit(self.map.floor.room.image, self.cam.apply(self.map.floor.room))

        for layer in self.rendLayers:
            for sprite in layer:
                try:
                    if pygame.Rect(0, 0, winWidth, winHeight).colliderect(self.cam.apply(sprite)):
                        self.win.blit(sprite.image, self.cam.apply(sprite))
                    # pygame.draw.rect(self.win, (200, 0, 0), self.cam.apply(sprite), 1)
                except AttributeError:
                    pass
        
        for fx in self.fxLayer:
            self.win.blit(fx.image, fx.rect)
        
        self.renderDarkness()

        for sprite in self.hudLayer:
            self.win.blit(sprite.image, sprite.rect)
        
        for sprite in self.overlayer:
            try:
                if sprite.active:
                    self.win.blit(sprite.image, sprite.rect)
            except AttributeError:
                self.win.blit(sprite.image, sprite.rect)
        
        if self.showFps:
            fpsText = fonts['caption1'].render(str(round(self.currentFps, 2)), self.antialiasing, (255, 255, 255))
            self.win.blit(fpsText, (1100, 5))
        
        if joystickEnabled:
            pos = self.player.cursor.pos
            size = self.player.cursor.size
            pygame.draw.rect(self.win, (200, 0, 0), (pos.x, pos.y, size.x, size.y))
        
        # shader_bloom_effect_array24(self.win, 0, fast_=True)
        
        # self.win.blit(self.player.getAttackMask(), (0, 0))
        
    def renderDarkness(self):
        darkness = pygame.Surface((winWidth, winWidth))
        lightRect = pygame.Rect(0, 0, self.player.lightSource.get_width(), self.player.lightSource.get_height())
        lightRect.center = self.cam.applyRect(self.player.moveRect).move(20, 20).topleft
        darkness.blit(self.player.lightSource, lightRect)
        for sprite in self.groups.lightSources:
            darkness.blit(sprite.sourceImg, self.cam.apply(sprite))

        self.win.blit(darkness, (0, 0), special_flags=pygame.BLEND_MULT)


    def checkHits(self):
        pygame.sprite.groupcollide(self.groups.colliders, self.groups.pProjectiles, False, True)
        # for e, projs in pygame.sprite.groupcollide(self.groups.enemies, self.groups.pProjectiles, False, False).items():
        #     for p in projs:
        #         p.hit(e)

        if self.player.stats.isDead():
            self.mixer.playFx('pHit')
            self.pause = True
            def cont():
                if True:
                    self.cam.target = self.player
                    self.pause = False
                    self.groups.enemies.empty()
                    self.map.switchLevel('cave1')
                    #self.player.reset()
                    self.fxLayer.empty()
                    for s in self.pSprites:
                        s.kill()
            def died():
                Button(self, (400, 400), groups = [self.pSprites, self.overlayer], text = "Continue", onClick=cont, instaKill = True, center = True, colors = (colors.orangeRed, colors.white))
                def end():
                    self.end = True
                Button(self, (400, 500), groups = [self.pSprites, self.overlayer], text = "Return to menu", onClick=end, instaKill = True, center = True, colors = (colors.orangeRed, colors.white))

            FadeOut(self, speed = 2.5, alpha = 40, color = colors.dark(colors.red, 60), startDelay = 540, noKill = True, onEnd = died)

    def unPause(self):
        self.pause = False
        self.pauseScreen.deactivate()

    def endgame(self):
        self.unPause()
        self.end = True

    def reset(self):
        for sprite in self.sprites:
            sprite.kill()
        for sprite in self.pSprites:
            sprite.kill()
        self.new()
        self.run()

    # def died(self):
        # Button(self, (400, 400), groups = [self.pSprites, self.overlayer], text = "Continue", onClick=self.cont, instaKill = True, center = True, colors = (colors.orangeRed, colors.white))
        # def end():
        #     self.end = True
        # Button(self, (400, 500), groups = [self.pSprites, self.overlayer], text = "Return to menu", onClick=end, instaKill = True, center = True, colors = (colors.orangeRed, colors.white))

    def quit(self):
        saveData(saveFile, self)
        pygame.quit()
        sys.exit()

    def runEvents(self):    
        ## Catch all events here
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.fullScreen:
                        self.win = pygame.display.set_mode((winWidth, winHeight))
                        self.fullScreen = False
                        pygame.display.set_icon(pygame.image.load(iconPath))
                    else:
                        self.quit()

        self.getFullScreen()
        if pygame.time.get_ticks() - self.lastCamTog >= 400 and checkKey(keySet['toggleCam']):
            self.toggleCam()
            self.lastCamTog = pygame.time.get_ticks()

    def getFps(self):
        self.currentFps = self.clock.get_fps() 
        return self.currentFps
    
    def toggleCam(self):
        self.cam.toggleTarget()

    def toggleFps(self):
        if self.showFps:
            self.showFps = False
        else:
            self.showFps = True
    
    def disableJoystick(self):
        self.joystickDisabled = False if self.joystickDisabled else True

    def toggleAalias(self):
        if self.antialiasing:
            self.antialiasing = False
        else:
            self.antialiasing = True
        
        self.pauseScreen.loadComponents()

    def getFullScreen(self):
        keys = pygame.key.get_pressed()
        if keys[keySet['fullScreen']]:
            if self.fullScreen:
                self.win = pygame.display.set_mode((winWidth, winHeight), winFlags)
                self.fullScreen = False
            else:
                self.win = pygame.display.set_mode((winWidth, winHeight), winFlags | pygame.FULLSCREEN)
                self.fullScreen = True
            pygame.display.set_icon(pygame.image.load(iconPath))
            #pygame.display.toggle_fullscreen()

    def getPause(self):
        if pygame.time.get_ticks() - self.lastPause >= 180:
            keys = pygame.key.get_pressed()
            if keys[keySet['pause']]:
                if self.pause:
                    self.unPause()
                else:
                    self.pause = True
                    self.pauseScreen.activate()

                self.lastPause = pygame.time.get_ticks()
                
    def getSprBylID(self, lID):
        for sprite in self.sprites:
            try:
                if sprite.lID == lID:
                    return sprite
            except:
                pass
        return False

    #### First menu loop ####
    def menuLoop(self):
        menus.main(self, True)

    def victoryLoop(self):
        menus.victoryLoop(self)

    def gameOver(self):
        menus.gameOver(self)

    def refresh(self, bg = False, isSurface = False):
        """Updates the background

        If bg is True, the provided image is used, otherwise the solid color black is used
        """
        if bg:
            if not isSurface:
                i = pygame.image.load(bg)
            else:
                i = bg
            self.win.blit(pygame.transform.scale(i, (winWidth, winHeight)).convert(), (0, 0))
        else:
            self.win.fill((0, 0, 0))

while __name__ == '__main__':
    game1 = Game()
    game1.run()
