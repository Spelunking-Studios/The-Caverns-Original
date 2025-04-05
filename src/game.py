import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pygame.sprite import Group

pygame.init()
import os
import random
import sys

from stgs import loadSave, saveFile
loadSave(saveFile)
from stgs import *
from fx import *
from levels import *
from menu import *
import objects
from overlay import *
from player import *
from sfx import *
from util import *
import menus
import hud


class Grouper:
    '''A class to control and manipulate multiple groups (pygame.group.Group)
    of game objects that is mainly designed for in code control'''

    def __init__(self):
        """Contains helpful groups for organizing different types of sprites"""
        # Create sprite groups here
        self.enemies = Group()
        self.lightSources = Group()
        self.colliders = Group()
        self.interactable = Group()  # Sprites that can be interacted with
        self.pProjectiles = Group()  # Player Projectiles
        self.eProjectiles = Group()  # Enemy Projectiles

    def getProximitySprites(self, sprite, proximity=300, groups=[]):
        """Returns a list of sprites that fall within the specified proximity\
        to the specified sprite.

        Arguments:
        ----------
        sprite: The sprite that the proximity will be around
        proximity (default=300): The max distance from the sprite another\
        sprite can be
        groups (default=[]): The groups in which entities can be
        found
        """
        groups = groups if isinstance(groups, list) else [groups]
        returnList = []

        for group in groups:
            for ent in group:
                ent_center = pygame.Vector2(ent.rect.center)
                sprite_center = pygame.Vector2(sprite.rect.center)
                dist = ent_center.distance_to(sprite_center)
                if dist <= proximity:
                    returnList.append(ent)

        return returnList

    def clearAll(self):
        for g in self.allGroups():
            g.empty()

    def killAll(self):
        for g in self.allGroups():
            for s in g:
                s.kill()

    def allGroups(self):
        return [self.__dict__[g] for g in self.__dict__ if isinstance(self.__dict__[g], Group)]


#### Game object ####
class Game:
    """Represents an instance of the game"""

    def __init__(self):
        """Initializes the game object"A Very Very Long Description.

        Groups each sprite type to perform targetted tasks
        All sprites go into the sprites group
        Sets up window, font, gravity, and cam
        Loads data for the game levels and the player   w
        """
        self.layer1 = Group()
        self.layer2 = Group()
        self.layer3 = Group()  # Non-Static Level Objects
        self.fxLayer = Group()
        self.hudLayer = Group()
        self.overlayer = Group()
        self.rendLayers = [self.layer1, self.layer2, self.layer3]
        self.mixer = getDriver()
        self.mixer.setMusicVolume(musicVolume) # between 0 and 1
        self.mixer.setFxVolume(fxVolume)
        self.antialiasing = aalias

        #pygame.display.set_icon(pygame.image.load(iconPath))
        self.display = Display()
        self.win = pygame.Surface((winWidth, winHeight))
        self.lastPause = pygame.time.get_ticks()
        self.lastReset = pygame.time.get_ticks()
        self.lastCamTog = pygame.time.get_ticks()
        self.currentFps = 0
        self.showFps = SHOWFPS
        self.joystickDisabled = joystickDisabled
        self.clock = pygame.time.Clock()
        self.loadingScreenShownBefore = LOADING_SCREEN_SHOWN_BEFORE
        self.new()

    def new(self):
        self.won = False
        self.end = False
        self.pause = False
        self.inInventory = False

        self.groups = Grouper()
        self.sprites = Group()
        # Pause Sprites
        self.pSprites = Group()
        # Inventory Sprites
        self.iSprites = Group()
        self.map = GameMap(self)
        print(globals()["GAME_STATE"].get("player_equipped_weapon", None))
        self.player = Player(
            self,
            asset('player/samplePlayer.png'),
            globals()["GAME_STATE"].get("player_inventory", None),
            globals()["GAME_STATE"].get("player_equipped_weapon", None),
        )
        self.inventoryOverlay = InventoryOverlay(self)
        self.pauseScreen = PauseOverlay(self)
        # self.mapScreen = MapOverlay(self)
        self.dialogueScreen = DialogueOverlay(self)
        self.statsInfo = hud.StatHud(self, border = asset("objects/dialog-frame.png")) 
        self.slots = hud.SlotsHud(self)
        self.updateT = pygame.time.get_ticks()
        self.cam = Cam(self, winWidth, winHeight)

    ####  Determines how the run will function ####
    def run(self):
        loadSave("game.store")
        self.mixer.playMusic(sAsset('intro.wav'))
        # self.menuLoop()
        self.map.loadFloor()
        self.mainLoop()
        self.mixer.stop()
        if self.won:
            self.victoryLoop()
        else:
            self.gameOver()

    #### Main game loop ####
    def mainLoop(self):
        self.dialogueScreen.dialogueFromText("""
            You enter the dark cave at the top of Mount Gorngeil. 
            You hear your footsteps reverberate off the walls that seem to wind endlessly into the depths.
                                                                                               
            You are alone                                    
            
        """)
        while not self.end:
            self.clock.tick(FPS)
            self.refresh()  # asset('objects/shocking.jpg'))

            # Updates Game
            self.runEvents()
            self.update()

    def update(self):
        self.getFps()
        self.getPause()
        if self.pause:
            self.pSprites.update()
        elif self.inInventory:
            self.iSprites.update()
        else:
            self.sprites.update()
            self.layer3.update()
            self.checkHits()
        self.overlayer.update()
        self.cam.update()

        self.render()

        self.display.update(self.win)

    def render(self):
        self.win.blit(self.map.floor.room.image, self.cam.apply(self.map.floor.room))

        for layer in self.rendLayers:
            for sprite in layer:
                # if hasattr(sprite, "image"):
                #     if pygame.Rect(0, 0, winWidth, winHeight).colliderect(self.cam.apply(sprite)):
                #         self.win.blit(sprite.image, self.cam.apply(sprite))
                sprite.draw(self.win, self.cam.applyRect)

        for fx in self.fxLayer:
            self.win.blit(fx.image, fx.rect)

        self.renderDarkness()

        for sprite in self.hudLayer:
            if isinstance(sprite, hud.SlotsHud):
                for slotHud in sprite.slots:
                    self.win.blit(slotHud.image, slotHud.rect)
            else:
                # self.win.blit(sprite.image, sprite.rect)
                sprite.draw(self.win)

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
            self.hudLayer.update()
            self.pause = True

            def cont():
                if True:
                    self.cam.target = self.player
                    self.pause = False
                    self.groups.enemies.empty()
                    self.map.switchLevel('cave1')
                    # self.player.reset()
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
                    if self.display.fullScreen:
                        self.display.toggle_fullscreen()
                    else:
                        self.quit()

        if pygame.time.get_ticks() - self.lastCamTog >= 400 and checkKey(keySet['toggleCam']):
            self.toggleCam()
            self.lastCamTog = pygame.time.get_ticks()

        # Inventory
        if checkKey(keySet["inventory"]) and self.inventoryOverlay.can_activate():
            self.toggleInventory()

    def getFps(self):
        self.currentFps = self.clock.get_fps()
        return self.currentFps

    def get_mouse_pos(self):
        return pygame.Vector2(pygame.mouse.get_pos()) - self.display.get_offset()

    def dt(self):
        return self.clock.get_time()*0.001

    def dt2(self):
        return self.clock.get_time()*0.06

    def toggleCam(self):
        self.cam.toggleTarget()

    def toggleFps(self):
        self.showFps = not self.showFps

    def toggleInventory(self):
        if self.inInventory:
            self.closeInventory()
        else:
            self.openInventory()

    def openInventory(self):
        self.inInventory = True
        self.inventoryOverlay.activate()

    def closeInventory(self):
        self.inInventory = False
        self.inventoryOverlay.deactivate()

    def disableJoystick(self):
        self.joystickDisabled = False if self.joystickDisabled else True

    def toggleAalias(self):
        self.antialiasing = not self.antialiasing
        self.pauseScreen.load_components()

    def getPause(self):
        if pygame.time.get_ticks() - self.lastPause >= 60:
            if checkKey(keySet['pause']):
                if self.pause:
                    self.unPause()
                else:
                    self.pause = True
                    self.pauseScreen.activate()

                self.lastPause = pygame.time.get_ticks()

    def getSprBylID(self, lID):
        for sprite in self.sprites:
            if getattr(sprite, "lID", False):
                return sprite
        return False

    def menuLoop(self):
        menus.main(self, True)

    def victoryLoop(self):
        menus.victoryLoop(self)

    def gameOver(self):
        menus.gameOver(self)

    def refresh(self, bg=False):
        """Updates the background

        If bg is True, the provided image is used, otherwise the solid color black is used
        """
        if bg:
            self.win.blit(pygame.transform.scale(bg, (winWidth, winHeight)), (0, 0))
        else:
            self.win.fill((0, 0, 0))

    def get_prefab(self, name):
        print(objects.__dict__)
        for k,v in objects.__dict__.items():
            if k == name:
                return v
