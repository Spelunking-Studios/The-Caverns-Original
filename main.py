import pygame

pygame.init()
import os
import random
import sys

from stgs import *
loadSave(saveFile)
from stgs import *
from camera import *
from fx import *
from levels import *
from menu import *
from objects import *
from overlay import *
from player import *
from sfx import *
import menus
import hud


#### Game object ####
class game:

    #### Initialize game object ####
    #
    # Groups each sprite type to perform targetted tasks
    # All sprites go into the sprites group
    # Sets up window, font, gravity, and cam
    # Loads data for the game levels and the player

    def __init__(self):
        self.layer1 = pygame.sprite.Group()
        self.layer2 = pygame.sprite.Group()
        self.fxLayer = pygame.sprite.Group()
        self.hudLayer = pygame.sprite.Group()
        self.overlayer = pygame.sprite.Group()
        self.rendLayers = [self.layer1, self.layer2]
        self.mixer = gameMixer()
        self.mixer.setMusicVolume(musicVolume) # between 0 and 1
        self.mixer.setFxVolume(fxVolume)
        self.antialiasing = aalias

        #pygame.display.set_icon(pygame.image.load(iconPath))
        self.win = pygame.display.set_mode((winWidth, winHeight), winFlags)
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(pygame.image.load(iconPath))
        self.font1 = pygame.font.Font(fAsset('PixelLove.ttf'), 48)
        self.font2 = pygame.font.Font(fAsset('PixelLove.ttf'), 23)
        self.menuFont = pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 15)
        self.gameOverFont = pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 60)
        self.victoryFont = pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 72)
        self.lastPause = pygame.time.get_ticks()
        self.lastReset = pygame.time.get_ticks()
        self.lastCamTog = pygame.time.get_ticks()
        self.points = 0
        self.gravity = 1.6
        self.currentFps = 0
        self.showFps = SHOWFPS
        self.joystickDisabled = joystickDisabled
        self.fullScreen = False
        self.clock = pygame.time.Clock()
        self.new()

    def new(self):
        self.won = False
        self.points = 0
        self.enemies = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.pSprites = pygame.sprite.Group()
        self.colliders = pygame.sprite.Group()
        self.dmgRects = pygame.sprite.Group()
        self.pBullets = pygame.sprite.Group()
        self.eBullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.lightSources = pygame.sprite.Group()
        self.levels = gameLevels
        self.player = player(self, asset('player/samplePlayer.png'))
            
        self.player.gravity = self.gravity
        self.end = False
        self.attempts = 0
        self.pause = False
        self.pauseScreen = pauseOverlay(self)
        self.mapScreen = mapOverlay(self)
        self.dialogueScreen = dialogueOverlay(self)
        self.statsInfo = hud.statHud(self)
        self.time = 0
        self.updateT = pygame.time.get_ticks()
        self.cam = cam(self, winWidth, winHeight)

    ####  Determines how the run will function ####
    def run(self):
        self.menuLoop()
        print("yay")
        #self.mixer.playMusic(asset('sounds/track 1.wav'))
        self.mainLoop()
        self.mixer.stop()
        if self.won:
            self.victoryLoop()
        else:
            self.gameOver()

    #### Controls how the levels will load ####
    def loadLevel(self, levelNum, *args):

        try:
            for obj in self.level.sprites:
                obj.kill()
        except:
            pass
        self.level = self.levels[levelNum-1] 
        self.level.load(self)
        
        self.cam.width, self.cam.height = self.level.rect.width, self.level.rect.height
        
        #try:
        self.player.setPos(self.level.entrance.rect.center)
        #except:
        #    print("No player Pos")

        self.time = 0

    def enemyInProximity(self, proximity=300): # This function is necessary for framerate saving when attacking with a weapon meshw 
        returnList = []
        for e in self.enemies:
            if pygame.Vector2(e.rect.center).distance_to(pygame.Vector2(self.player.rect.center)) <= proximity:
                returnList.append(e)
        return returnList

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
        self.win.blit(self.level.image, self.cam.apply(self.level))

        for layer in self.rendLayers:
            for sprite in layer:
                try:
                    self.win.blit(sprite.image, self.cam.apply(sprite))
                    pygame.draw.rect(self.win, (200, 0, 0), sprite.rect)
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
            fpsText = fonts['6'].render(str(self.currentFps), self.antialiasing, (255, 255, 255))
            self.win.blit(fpsText, (1100, 5))
        
        if joystickEnabled:
            pos = self.player.cursor.pos
            size = self.player.cursor.size
            pygame.draw.rect(self.win, (200, 0, 0), (pos.x, pos.y, size.x, size.y))
        
        # self.win.blit(self.player.getAttackMask(), (0, 0))
        
    def renderDarkness(self):
        darkness = pygame.Surface((winWidth, winWidth))
        lightRect = pygame.Rect(0, 0, self.player.lightSource.get_width(), self.player.lightSource.get_height())
        lightRect.center = self.cam.applyRect(self.player.moveRect).move(20, 20).topleft
        darkness.blit(self.player.lightSource, lightRect)
        for sprite in self.lightSources:
            darkness.blit(sprite.sourceImg, self.cam.apply(sprite))
        self.win.blit(darkness, (0, 0), special_flags=pygame.BLEND_MULT)


    def checkHits(self):
        
        # for e in self.enemies:
        #     if self.player.maskCollide(e.rect):
        #         try:
        #             e.takeDamage(self.player.damage)
        #         except:
        #             e.health -= self.player.damage
        #         if e.health <= 0:
        #             e.deathSound()
        #             self.level.points += e.points
        #             self.level.enemyCnt -= 1

        pygame.sprite.groupcollide(self.colliders, self.pBullets, False, True)
        pygame.sprite.groupcollide(self.colliders, self.eBullets, False, True)

        items = pygame.sprite.spritecollide(self.player, self.items, True)

        # r2 = self.level.door.rect ## This section checks door collision with player mask
        # if self.player.mask.overlap(pygame.mask.Mask(r2.size, True), (r2.x-self.player.rect.x,r2.y-self.player.rect.y)):
        #     self.pause = True
        #     self.mixer.playFx('menu3')
        #     fadeOut(self, speed = 5, alpha = 40, onEnd = lambda:self.nextLevel())

        # if player dies:
        #     self.mixer.playFx('pHit')
        #     self.pause = True
        #     fadeOut(self, speed = 2.5, alpha = 40, color = colors.dark(colors.red, 60), startDelay = 540, noKill = True, onEnd = self.died)

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
        # button(self, (400, 400), groups = [self.pSprites, self.overlayer], text = "Continue", onClick=self.cont, instaKill = True, center = True, colors = (colors.orangeRed, colors.white))
        # def end():
        #     self.end = True
        # button(self, (400, 500), groups = [self.pSprites, self.overlayer], text = "Return to menu", onClick=end, instaKill = True, center = True, colors = (colors.orangeRed, colors.white))
    
    def getLvlNum(self, offSet=0):
        return self.levels.index(self.level) + 1 + offSet

    def nextLevel(self):
        self.cam.target = self.player
        if DEBUG:
            try:
                self.loadLevel(self.levels.index(self.level) + 2)
                fadeIn(self, speed = 20, onEnd = lambda:self.unPause())
            except IndexError:
                self.end = True
                self.won = True
        else:
            try:
                self.loadLevel(self.levels.index(self.level) + 2)
                fadeIn(self, onEnd = lambda:self.unPause())
            except:
                self.end = True
                self.won = True

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
        menus.main(self)

    def victoryLoop(self):
        menus.victoryLoop(self)

    def gameOver(self):
        menus.gameOver(self)

    def refresh(self, bg = False):
        if bg:
            self.win.blit(pygame.transform.scale(pygame.image.load(bg), (winWidth, winHeight)).convert(), (0, 0))
        else:
            self.win.fill((0, 0, 0))

#### Creates and runs game ####
game1 = game()
while __name__ == '__main__':
    game1.run()
