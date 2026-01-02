from src import util, fx
import pygame
import math
from src.overlay import *
from src.menu import *
from src.stgs import *
import src.util.colors as colors

class Menu:
    def __init__(self, game):
        self.game = game
        self.comps = pygame.sprite.Group()
        self.hudlayer = pygame.sprite.Group()
        self.running = True
        self.color_transition_speed = 0.001
        
        self.bg = pygame.image.load(asset("loading screen (blur+noise).jpeg")).convert_alpha()
        self.bg.fill((50, 50, 50), special_flags=pygame.BLEND_RGBA_MIN)

    def run(self):
        while self.running:
            self.game.display.set_ambient(220, 
                200+30*math.sin(now()*self.color_transition_speed),
                200+30*math.sin(now()*self.color_transition_speed+1.5)
            )
            self.game.clock.tick(FPS)
            self.game.window_events()
            self.game.refresh(self.bg)
            self.comps.update()
            self.update()
            self.render()
            self.game.display.update(self.game.bg, self.game.fg)
    
    def render(self):
        for s in self.hudlayer:
            self.game.fg.blit(s.image, s.rect)
    
    def update(self):
        pass

class CompendiumMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        
        #MenuItem(game, (x, y), asset(''), desc='', text=''),
        self.returnButton = ImageButton(game, (game.width()-240, 70), text="Return", center = True, groups = [self.comps, self.hudlayer])
        self.comps.add([Text('instruction-text', "use your mouse to aim the player \nClick to attack\n WASD to move\nTAB for inventory\nP for pause menu\nSPACE to end dialogue", colors.orangeRed, game.antialiasing, (80, 160), True)])
        self.comps.add([Text('main-title1', TITLE,  colors.orangeRed, game.antialiasing, (30,game.height() - 70), False)])
        self.hudlayer.add([c for c in self.comps if c not in self.hudlayer])
        self.run()
    
    def update(self):
        if self.returnButton.clicked:
            self.running = False

        if checkKey(keySet['start']):
            self.running = False

class SettingsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.returnButton = ImageButton(
            game,
            (game.width()-240, 70),
            text = "Return",
            center = True,
            colors=(colors.yellow, colors.white),
            groups = [self.comps, self.hudlayer]
        )
        self.audioSlider1 = SettingSlider(
            game,
            (100, 350),
            addGroups = [self.comps, self.hudlayer]

        )
        self.audioSlider2 = SettingSlider(
            game,
            (100, 500),
            addGroups = [self.comps, self.hudlayer]
        )
        fpsButton = ImageButton(
            game,
            (800, 250),
            text = 'Toggle FPS', 
            onClick = game.toggleFps,
            groups = [self.comps, self.hudlayer],
        )
        aaliasButton = ImageButton(
            game,
            (800, 330),
            text = 'Toggle Anti - Aliasing',
            onClick = game.toggleAalias,
            groups = [self.comps, self.hudlayer],
        )
        joystickButton = ImageButton(
            game,
            (800, 530),
            text = 'Joystick Disable',
            onClick = game.disableJoystick,
            groups = [self.comps, self.hudlayer],
        )
        self.hudlayer.add([
            Text(
                'title1',
                'Audio Control',
                colors.orangeRed,
                game.antialiasing,
                (75, 250)
            ),
            Text(
                'caption1',
                'Music Volume',
                colors.orangeRed,
                game.antialiasing,
                (75, 325)
            ),
            Text(
                'caption1',
                'Fx Volume',
                colors.orangeRed,
                game.antialiasing,
                (75, 475)
            ),
            Text(
                'main-title1',
                TITLE,
                colors.orangeRed,
                game.antialiasing,
                (30,30)
            )
        ])
        
        i = 0
        for mode in self.game.display.get_modes():
            def passthrough(v):
                def set_mode():
                    game.display.set_mode(v)
                    self.returnButton = ImageButton(
                        game,
                        (game.width()-240, 70),
                        text = "Return",
                        center = True,
                        colors=(colors.yellow, colors.white),
                        groups = [self.comps, self.hudlayer]
                    )
                return set_mode
            ImageButton(
                game,
                (100 + i*200, 630),
                text = "Size: " + str(mode),
                onClick = passthrough(mode),
                groups = [self.comps, self.hudlayer],
            )
            i += 1
        self.audioSlider1.setRatio(game.mixer.musicVolume)
        self.audioSlider2.setRatio(game.mixer.fxVolume)
        self.run()

    def applyComps(self):
        self.game.mixer.setMusicVolume(self.audioSlider1.get_ratio())
        self.game.mixer.setFxVolume(self.audioSlider2.get_ratio())

    def update(self):
        self.applyComps()
        if self.returnButton.clicked:
            self.running = False

        #if checkKey(keySet['start']):
        #    self.game.map.loadFloor()
        #    self.running = False

class SaveContinueMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        
        #MenuItem(game, (x, y), asset(''), desc='', text=''),
        self.continue_btn = ImageButton(game, (0, 340), text="Continue", center = True, colors = (colors.rgba(colors.yellow, 255), colors.white), wh=(300, 60), rounded = True)
        self.new_game_btn = ImageButton(game, (0, 460), text="New Game", center=True, colors = (colors.yellow, colors.white), wh=(250, 60))
        self.comps.add([
            self.continue_btn,
            self.new_game_btn
        ])
        for c in self.comps:
            c.rect.centerx = game.width()/2
        self.hudlayer.add([c for c in self.comps if c not in self.hudlayer])
        self.game.pSprites = pygame.sprite.Group()
        self.title = pygame.image.load(asset("objects/TheCaverns2.png"))
        self.title.set_colorkey((255,255,255))
        self.title_rect = pygame.Rect(0, -80, self.title.get_width(), self.title.get_height())
        self.title_rect.centerx = game.width()/2
        self.swordImg = pygame.transform.scale(pygame.image.load(asset('screens/part_one.png')), (440, 100))
        self.swordRect = pygame.Rect(0, 170, self.swordImg.get_width(), self.swordImg.get_height())
        self.swordRect.centerx = game.width()/2 + 8
        self.fx = pygame.sprite.Group()
        self.run()
    
    def update(self):
        if self.continue_btn.clicked:
            fx.FadeOut(self.game, onEnd=self.turnoff, groups = self.fx, noKill=True)

        if self.new_game_btn.clicked:
            self.game.wipe_save()
            fx.FadeOut(self.game, onEnd=self.turnoff, groups = self.fx, noKill=True)

        for f in self.fx:
            f.update()

    def turnoff(self):
        self.running = False

    def render(self):
        super().render()
        self.game.fg.blit(self.title, self.title_rect)
        self.game.fg.blit(self.swordImg, self.swordRect)
        for fx in self.fx:
            fx.draw(self.game.fg, None)
        


class CreditsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.returnButton = ImageButton(game, (0, game.height() - 100), text="Return", center = True, colors = (colors.yellow, colors.white), groups = [self.comps, self.hudlayer])
        menuItems = [ Text("title1", "─────Credits─────", colors.orangeRed, game.antialiasing, (0, 50)),
            Text("credits-names", "Benjamin Landon                                             Code", colors.orangeRed, game.antialiasing, (0, 225)),
            Text("credits-names", "Luke Gonsalves        Code, Design, Graphics", colors.orangeRed, game.antialiasing, (0, 300)),
            Text("credits-names", "Matthew Hosier                     Design, Graphics", colors.orangeRed, game.antialiasing, (0, 375)),
        ]
        # Pre-calculate half of the windows width because division is slow
        halfWinWidth = game.width() / 2
        for item in menuItems:
            item.rect.centerx = halfWinWidth
        
        self.hudlayer.add(menuItems)
        
        self.run()
    def update(self):
        if self.returnButton.clicked:
            self.running = False

        if checkKey(keySet['start']):
            self.running = False

class Main(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.startButton = ImageButton(game, (0, 340), text="Play", center = True, colors = (colors.yellow, colors.white), wh=(300, 60), groups = [self.comps, self.hudlayer])
        self.settingsButton = ImageButton(game, (0, 580), text="Settings", center=True, colors = (colors.yellow, colors.white), groups = [self.comps, self.hudlayer])
        self.instructionsButton = ImageButton(game, (0, 460), text="Instructions", center=True, colors = (colors.yellow, colors.white), wh=(250, 60), groups = [self.comps, self.hudlayer])
        self.creditsButton = ImageButton(game, (200, 580), text="Credits", center = True, colors = (colors.yellow, colors.white), groups = [self.comps, self.hudlayer])

        self.settingsButton.rect.centerx, self.creditsButton.rect.centerx = game.width() / 2, game.width() / 2

        swordImg = pygame.transform.scale(pygame.image.load(asset('screens/part_one.png')), (320, 320))
        swordRect = pygame.Rect(0, 65, swordImg.get_width(), swordImg.get_height())
        swordRect.centerx = game.width()/2
        text1 = Text('subtitle1', 'Press S to Start', colors.orangeRed, game.antialiasing,(30, 30))
        text2 = Text('main-title1', TITLE, colors.orangeRed, game.antialiasing, (0, 30))
        text2.rect.centerx = game.width()/2


def main(game, loadingScreenOn = False):
    lssb = game.loadingScreenShownBefore
    if loadingScreenOn:
        game.loadingScreenShownBefore = True
        # Loading screen
        toMainMenuButton = ImageButton(game, (0, game.height() - 100), text = "Continue", center = True, colors = (colors.yellow, colors.white))
        toMainMenuButton.rect.centerx = game.width() / 2
        loadingScreenBGSurface = pygame.image.load(asset("loading screen (blur+noise).jpeg")).convert_alpha()
        loadingScreenBGSurface.fill((50, 50, 50), loadingScreenBGSurface.get_rect(), special_flags=pygame.BLEND_RGBA_MIN)
    
        loadingText = []
        tti = 0
        ti = 1
        for t in LOADING_TEXT:
            text = Text(
                "2",
                t,
                colors.rgba(colors.orangeRed, 50),
                game.antialiasing,
                (10, 10 * ti)
            )
            text.image.set_alpha(0)
            loadingText.append(text)
            loadingText[tti].rect.centerx = game.width() / 2
            ti += 4
            tti += 1
        loadingLinesShowed = 1
        loadingLinesTimings = [0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005]
        tmmbt = "Skip"
        if not lssb:
            tmmbt = "Continue"
        toMainMenuButton = ImageButton(game, (0, game.height() - 100), text = tmmbt, center = True, colors = (colors.yellow, colors.white))
        toMainMenuButton.rect.centerx = game.width() / 2
    else:
        toMainMenuButton.clicked = True

    startButton = ImageButton(game, (0, 340), text="Start", center = True, colors = (colors.rgba(colors.yellow, 255), colors.white), wh=(300, 60), rounded = True)
    settingsButton = ImageButton(game, (0, 580), text="Settings", center=True, colors = (colors.yellow, colors.white))
    instructionsButton = ImageButton(game, (0, 460), text="Instructions", center=True, colors = (colors.yellow, colors.white), wh=(250, 60))
    creditsButton = ImageButton(game, (200, 580), text="Credits", center = True, colors = (colors.yellow, colors.white))

    settingsButton.rect.centerx = (game.width() / 2) - (settingsButton.rect.width / 2) - 10
    creditsButton.rect.centerx = (game.width() / 2) + (creditsButton.rect.width / 2) + 10

    comps = pygame.sprite.Group(startButton, instructionsButton) # Stands for components fyi
    for c in comps:
        c.rect.centerx = game.width()/2
    swordImg = pygame.transform.scale(pygame.image.load(asset('screens/part_one.png')), (440, 100))
    swordRect = pygame.Rect(0, 170, swordImg.get_width(), swordImg.get_height())
    swordRect.centerx = game.width()/2 + 8
    text1 = Text('subtitle1', 'Press S to Start', colors.orangeRed, game.antialiasing,(30, 30))
    # text2 = Text('main-title1', TITLE, colors.orangeRed, game.antialiasing, (0, 30))
    title = pygame.image.load(asset("objects/TheCaverns2.png"))
    title.set_colorkey((255,255,255))
    titleRect = pygame.Rect(0, -80, title.get_width(), title.get_height())
    titleRect.centerx = game.width()/2
    #text3 = Text('title2', 'Created by LGgameLAB (with help)', colors.orangeRed, game.antialiasing, (0, 110))
    #text3.rect.centerx = game.width()/2

    #tv = 0
    color_transition_speed = 0.001
    while True:
        game.clock.tick(FPS)
        #pygame.time.delay(50)

        game.window_events()
        #tv += 255 / loadingCounter
        #pygame.draw.rect(
        #    loadingScreenBGSurface,
        #    (0, 0, 0, tv),
        #    (0, 0, game.width(), game.height())
        #)
        game.refresh(loadingScreenBGSurface)
        
        comps.update()
        creditsButton.update()
        settingsButton.update()

        iloadingLinesEloadingTextLen = int(loadingLinesShowed) == len(loadingText)

        if toMainMenuButton.clicked:
            game.display.set_ambient(220, 
                200+30*math.sin(now()*color_transition_speed),
                200+30*math.sin(now()*color_transition_speed+1.5)
            )
            for comp in comps:
                game.fg.blit(comp.image, comp.rect)
            game.fg.blit(creditsButton.image, creditsButton.rect)
            game.fg.blit(settingsButton.image, settingsButton.rect)

            if startButton.clicked:
                break
            
            if settingsButton.clicked:
                SettingsMenu(game)
                settingsButton.reset()
            
            if instructionsButton.clicked:
                CompendiumMenu(game)
                instructionsButton.reset()
            
            if creditsButton.clicked:
                CreditsMenu(game)
                creditsButton.reset()
        
            #game.fg.blit(text1.image, text1)
            game.fg.blit(title, titleRect)
            game.fg.blit(swordImg, swordRect)

            keys = pygame.key.get_pressed()

            if keys[keySet['start']]:
                break
        else:
            for i in range(int(loadingLinesShowed)):
                game.fg.blit(loadingText[i].image, loadingText[i])
                loadingText[i].image.set_alpha(min(255, loadingText[i].image.get_alpha()+1))
            if loadingLinesShowed <= len(loadingText):
                loadingLinesShowed += loadingLinesTimings[int(loadingLinesShowed)] #0.05
            toMainMenuButton.update()
            if iloadingLinesEloadingTextLen or lssb:
                if toMainMenuButton.text != "Continue" and iloadingLinesEloadingTextLen:
                    toMainMenuButton.setText("Continue")
            game.fg.blit(toMainMenuButton.image, toMainMenuButton.rect)
            #for t in loadingText:
            #    game.fg.blit(t.image, t)
        
        game.display.update(game.bg, game.fg)

def gameOver(game):
    restartButton = ImageButton(game, (game.width()/2, game.height()/2), text="Back to Menu", center = True, colors = (colors.yellow, colors.white))
    buttons = pygame.sprite.Group(restartButton)
    while True:
        game.clock.tick(FPS)
        
        game.window_events()
        game.refresh()

        buttons.update()
        for btn in buttons:
            game.fg.blit(btn.image, btn.rect)

        if restartButton.clicked:
            game.reset()
            break
        
        
        text1 = fonts['gameover'].render('Game Over', game.antialiasing, colors.dark(colors.orangeRed, 20))
        text2 = fonts['title1'].render("Score: " + str(game.points), game.antialiasing, (colors.yellow))
        
        game.fg.blit(text1, (50,50))
        game.fg.blit(text2, (800, 70))
        
        game.display.update(None, game.fg)

def victoryLoop(game):
    text1 = fonts['victory'].render('You Win', game.antialiasing, colors.yellow, 20)
    text2 = fonts['title1'].render("To be continued...", game.antialiasing, (colors.yellow))
    game.mixer.playFx('yay')
    while True:
        game.clock.tick(FPS)
        
        game.window_events()
        game.refresh()

        
        game.fg.blit(text2, (800, 70))
        game.fg.blit(text1, (game.width()/2 - text1.get_width()/2 ,30))
        
        game.display.update(game.bg, game.fg)
