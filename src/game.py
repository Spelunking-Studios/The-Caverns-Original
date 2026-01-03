import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pygame.sprite import Group

import pymunk
import pymunk.pygame_util

pygame.init()
import os
import random
import sys

from .stgs import loadSave, saveFile
from .stgs import *
loadSave(saveFile)
from src.levels import GameMap
from src.menu import *
from src import objects
from src import prefabs
from src.overlay import *
from src.player import *
from src.sfx import *
from src.fx import FadeOut, FadeIn
from src.util import *
from src import menus
from src import hud


#### Game object ####
class Game:
    """Represents an instance of the game"""

    def __init__(self):
        """Initializes the game object
        Sets up window, font, gravity, and cam
        """
        self.mixer = getDriver()
        self.mixer.setMusicVolume(musicVolume) # between 0 and 1
        self.mixer.setFxVolume(fxVolume)
        self.antialiasing = aalias

        #pygame.display.set_icon(pygame.image.load(iconPath))
        self.display = Display(self)
        self.clock = pygame.time.Clock()
        self.bg = pygame.Surface(self.display.resolution, pygame.SRCALPHA)
        # Create a separate render target for the elements not covered by the darkness
        self.fg = pygame.Surface(self.bg.get_size(), pygame.SRCALPHA)
        self.lastPause = now()
        self.lastReset = now()
        self.lastCamTog = now()
        self.currentFps = 0
        self.showFps = SHOWFPS
        self.joystickDisabled = joystickDisabled
        self.loadingScreenShownBefore = LOADING_SCREEN_SHOWN_BEFORE
        if globals()["SETTINGS"].get("display_mode", False):
            self.display.set_mode(globals()["SETTINGS"].get("display_mode", None))

    def new(self):
        # Global Game Variables
        self.won = False
        self.end = False
        self.pause = False
        self.inInventory = False
        self.hard_mode = False
        self.points = 0

        # Physics Engine
        self.space = pymunk.Space()
        self.space.damping = 0.0002
        self.handler = Handler(self)
        self.pymunk_options = pymunk.pygame_util.DrawOptions(self.bg)
        self.pymunk_options.transform = pymunk.Transform.translation(0, 0)
        
        # Sprite Groups
        self.groups = Grouper()
        self.layer1 = Group()
        self.layer2 = Group()
        self.layer3 = Group()  # Non-Static Level Objects
        self.fxLayer = Group()
        self.hudLayer = Group()
        self.overlayer = Group()
        self.rendLayers = [self.layer1, self.layer2, self.layer3]
        self.sprites = Group()
        self.pSprites = Group() # Pause Sprites
        self.iSprites = Group() # Inventory Sprites
        self.display.empty_lights() # Removes any lights from previous game

        # Game entities
        self.map = GameMap(self)
        self.alert_hud = hud.AlertHud(self)
        self.player = Player(
            self,
            globals()["GAME_STATE"].get("player_inventory", None),
            globals()["GAME_STATE"].get("player_equipped_weapon", None),
        )
        self.cam = Camera(self, self.width(), self.height())
        self.progress = globals()["GAME_STATE"].get("progress", {
            "save_point": None,
            "chests_opened": [],
            "notes_collected": [],
            "events_triggered": []
        })
        self.inventoryOverlay = InventoryOverlay(self)
        self.pauseScreen = PauseOverlay(self)
        self.hoverOverlay = HoverOverlay(self)
        self.dialogueScreen = DialogueOverlay(self)
        self.statsInfo = hud.StatHud(self, border = asset("objects/dialog-frame.png")) 
        self.slots = hud.SlotsHud(self)
        self.updateT = now()
        
        
    ####  Determines how the run will function ####
    def run(self):
        # loadSave("game.store")
        if not DEBUG:
            self.menuLoop()
        menus.SaveContinueMenu(self) 
        self.new()
        self.mainLoop()
        self.mixer.stop()
        self.player.kill()
        if self.won:
            self.victoryLoop()
        else:
            self.gameOver()

    #### Main game loop ####
    def mainLoop(self):
        self.map.loadFloor()
        self.mixer.playMusic(sAsset('Adventure-Piano.mp3'))


        # Run pre-first frame loading
        for sprite in self.sprites:
            sprite.start()

        self.display.set_ambient_lighting((10, 10, 10))

        while not self.end:
            dt = self.clock.tick(FPS)
            self.refresh()  

            # Updates Game
            self.window_events()
            self.update(dt)

    def update(self, dt):
        self.get_fps()
        self.get_pause()
        if self.pause:
            self.pSprites.update()
        elif self.inInventory:
            self.iSprites.update()
            self.game_events()
        else:
            self.space.step(1/FPS)
            self.sprites.update()
            self.layer3.update()
            self.game_events()
        self.overlayer.update()
        self.cam.update()

        self.render()

        # if DEBUG:
        pygame.display.set_caption(TITLE + " " + str(self.currentFps))

    def render(self):

        self.bg.blit(self.map.floor.room.image, self.cam.apply(self.map.floor.room))

        for layer in self.rendLayers:
            for sprite in layer:
                # if hasattr(sprite, "image"):
                #     if pygame.Rect(0, 0, winWidth, winHeight).colliderect(self.cam.apply(sprite)):
                #         self.bg.blit(sprite.image, self.cam.apply(sprite))
                sprite.draw(self.bg, self.cam.applyRect)


        for fx in self.fxLayer:
            self.bg.blit(fx.image, fx.rect)

        # image = pygame.surface.Surface((self.width(), self.height()), pygame.SRCALPHA)
        # image.fill((100, 0, 0))
        # image.set_alpha(5)
        # self.bg.blit(image, (0, 0))
        

        # self.bg.fill((200, 0, 0, 100))


        # Everything beyond here is drawn on a separate target surface
        # so that the shader library can distinguish what to cover with light and what not to
        for sprite in self.hudLayer:
            sprite.draw(self.fg)

        for sprite in self.overlayer:
            if hasattr(sprite, "active"):
                if sprite.active:
                    sprite.draw(self.fg)

        if DEBUG_PHYSICS:
            self.space.debug_draw(self.pymunk_options)

        if self.showFps:
            fpsText = fonts['caption1'].render(str(self.currentFps), self.antialiasing, (255, 255, 255))
            self.fg.blit(fpsText, (1100, 5))
        
        if joystickEnabled and DEBUG:
            pos = self.player.cursor.pos
            size = self.player.cursor.size
            pygame.draw.rect(self.fg, (200, 0, 0), (pos.x, pos.y, size.x, size.y))


        self.display.update(self.bg, self.fg)

    
    # def renderDarkness(self):
    #     darkness = pygame.Surface((self.width(), self.height()))
    #     darkness.fill((255,255,255))
    #     self.player.draw_darkness(darkness, self.cam.applyRect)
    #     for sprite in self.groups.lightSources:
    #         darkness.blit(sprite.image, self.cam.apply(sprite))
        # self.bg.blit(darkness, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

    def count_particles(self):
        print(sum(p.get_batch_size() for p in self.groups.particle_emitters))

    def game_events(self):
        if now() - self.lastCamTog >= 400 and checkKey(keySet['toggleCam']):
            self.toggleCam()
            self.lastCamTog = now()

        # Inventory
        if checkKey(keySet["inventory"]) and self.inventoryOverlay.can_activate():
            self.toggleInventory()

        if self.player.stats.isDead():
            self.mixer.playFx('pHit')
            self.hudLayer.update()
            self.pause = True
            self.save()

            def cont():
                print("continuing the game")
                if True:
                    # Save data
                    player_inventory = self.player.inventory.serialize()
                    globals()["GAME_STATE"]["player_inventory"] = player_inventory
                    globals()["GAME_STATE"]["progress"] = self.progress
                    self.new()
                    self.mainLoop()

            def died():
                prefabs.RedButton(self, (400, 400), "Continue", cont)
                def end():
                    print("psych not continuing")
                    self.end = True
                prefabs.RedButton(self, (400, 500), "Return to menu", end)

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
        self.sprites.empty()
        for sprite in self.pSprites:
            sprite.kill()
        self.pSprites.empty()
        self.groups.killAll()
        self.new()
        self.run()

    def quit(self):
        self.save()
        pygame.quit()
        sys.exit()

    def save(self, wipe=False):
        saveData(saveFile, self, wipe)

    def wipe_save(self):
        globals()["GAME_STATE"] = {}

    def load_save(self):
        loadSave(saveFile)

    def width(self):
        return self.bg.get_width()

    def height(self):
        return self.bg.get_height()

    def size(self):
        return self.width(), self.height()

    def window_events(self):
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
                        self.toggle_pause()



    def get_fps(self):
        self.currentFps = round(self.clock.get_fps(), 2)
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

    def toggle_pause(self):
        if now() - self.lastPause >= 160:
            if self.pause:
                self.unPause()
            else:
                self.pause = True
                self.pauseScreen.activate()

            self.lastPause = now()


    def get_pause(self):
        if checkKey(keySet['pause']):
            self.toggle_pause()

    def getSprBylID(self, lID):
        for sprite in self.sprites:
            if getattr(sprite, "lID", False):
                return sprite
        return False

    def menuLoop(self):
        self.mixer.playMusic(sAsset('intro.wav'))
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
            self.bg.blit(pygame.transform.scale(bg, self.size()), (0, 0))
        else:
            self.bg.fill((0, 0, 0, 0))

        self.fg.fill((0,0,0,0))

    def get_prefab(self, name):
        # Look in objects module
        for k,v in objects.__dict__.items():
            if k == name:
                return v
        
        # Look in defined prefabs
        for k,v in prefabs.__dict__.items():
            if k == name:
                return v
