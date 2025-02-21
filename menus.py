# import PygameShader
# from PygameShader import gaussianBlur5x5, shader
# with open("pygameshaderdoc.txt", "w") as f:
#     f.write(shader.__file__)
import pygame
from overlay import *
from menu import *
from stgs import *
import colors

class Menu:
    def __init__(self, game):
        self.game = game
        self.comps = pygame.sprite.Group()
        self.layer1 = pygame.sprite.Group()
        self.running = True
        self.bg = pygame.image.load(asset("loading screen.jpeg")).convert_alpha()
        self.bg.fill((50, 50, 50), special_flags=pygame.BLEND_RGBA_MIN)
        # gaussianBlur5x5.canny_blur5x5_surface24_c(self.bg)
        # shader.blur(self.bg, 2)
        # shader.bloom(self.bg, 5, False)
        # shader.swirl(self.bg, 95)
    def run(self):
        while self.running:
            pygame.display.set_caption(TITLE + f" {self.game.getFps()}")
            self.game.clock.tick(FPS)
            self.game.runEvents()
            self.game.refresh(self.bg)
            self.comps.update()
            self.update()
            self.render()
            pygame.display.update()
    
    def render(self):
        for s in self.layer1:
            self.game.win.blit(s.image, s.rect)
    
    def update(self):
        pass

class CompendiumMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        
        #MenuItem(game, (x, y), asset(''), desc='', text=''),
        self.returnButton = Button(game, (winWidth-240, 70), text="Return", center = True, groups = [self.comps, self.layer1])
        self.comps.add([Text('description1', "descText", colors.yellow, game.antialiasing, (winWidth- 1200,winHeight - 340), True)])
        self.comps.add([Text('main-title1', TITLE,  colors.yellow, game.antialiasing, (30,winHeight - 70), False)])
        self.layer1.add([c for c in self.comps if c not in self.layer1])
        self.run()
    
    def update(self):
        if self.returnButton.clicked:
            self.running = False

        if checkKey(keySet['start']):
            self.game.map.loadFloor()
            self.running = False

class SettingsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.returnButton = Button(
            game,
            (winWidth-240, 70),
            text = "Return",
            center = True,
            colors=(colors.yellow, colors.white),
            groups = [self.comps, self.layer1]
        )
        self.audioSlider1 = SettingSlider(
            game,
            (100, 350),
            addGroups = [self.comps, self.layer1]
        )
        self.audioSlider2 = SettingSlider(
            game,
            (100, 500),
            addGroups = [self.comps, self.layer1]
        )
        fpsButton = Button(
            game,
            (800, 250),
            text = 'Toggle FPS', 
            onClick = game.toggleFps,
            groups = [self.comps, self.layer1],
        )
        aaliasButton = Button(
            game,
            (800, 330),
            text = 'Toggle Anti - Aliasing',
            onClick = game.toggleAalias,
            groups = [self.comps, self.layer1],
        )
        joystickButton = Button(
            game,
            (800, 530),
            text = 'Joystick Disable',
            onClick = game.disableJoystick,
            groups = [self.comps, self.layer1],
        )
        self.layer1.add([
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

class CreditsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.returnButton = Button(game, (0, winHeight - 100), text="Return", center = True, colors = (colors.yellow, colors.white), groups = [self.comps, self.layer1])
        menuItems = [ Text("title1", "Credits", colors.orangeRed, game.antialiasing, (0, 50)),
            Text("subtitle1", "~~~ Graphics ~~~", colors.orangeRed, game.antialiasing, (0, 150)),
            Text("3", "Matthew Hosier", colors.orangeRed, game.antialiasing, (0, 225)),
            Text("subtitle1", "~~~ Code ~~~", colors.orangeRed, game.antialiasing, (0, 275)),
            Text("3", "Luke Gonsalves", colors.orangeRed, game.antialiasing, (0, 350)),
            Text("3", "Ben Landon", colors.orangeRed, game.antialiasing, (0, 425))
        ]
        # Pre-calculate half of the windows width because division is slow
        halfWinWidth = winWidth / 2
        for item in menuItems:
            item.rect.centerx = halfWinWidth
        
        self.layer1.add(menuItems)
        self.run()

    def update(self):
        if self.returnButton.clicked:
            self.running = False

        if checkKey(keySet['start']):
            self.game.map.loadFloor()
            self.running = False

class Main(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.startButton = Button(game, (0, 340), text="Start", center = True, colors = (colors.yellow, colors.white), wh=(300, 60), groups = [self.comps, self.layer1])
        self.settingsButton = Button(game, (0, 580), text="Settings", center=True, colors = (colors.yellow, colors.white), groups = [self.comps, self.layer1])
        self.instructionsButton = Button(game, (0, 460), text="Instructions", center=True, colors = (colors.yellow, colors.white), wh=(250, 60), groups = [self.comps, self.layer1])
        self.creditsButton = Button(game, (200, 580), text="Credits", center = True, colors = (colors.yellow, colors.white), groups = [self.comps, self.layer1])

        self.settingsButton.rect.centerx, self.creditsButton.rect.centerx = winWidth / 2, winWidth / 2

        swordImg = pygame.transform.scale(pygame.image.load(asset('player/sw1.png')), (320, 320))
        swordRect = pygame.Rect(0, 65, swordImg.get_width(), swordImg.get_height())
        swordRect.centerx = winWidth/2
        text1 = Text('subtitle1', 'Press S to Start', colors.orangeRed, game.antialiasing,(30, 30))
        text2 = Text('main-title1', TITLE, colors.orangeRed, game.antialiasing, (0, 30))
        text2.rect.centerx = winWidth/2


def main(game, loadingScreenOn = False):
    lssb = game.loadingScreenShownBefore
    if loadingScreenOn:
        game.loadingScreenShownBefore = True
    # Loading screen
    toMainMenuButton = Button(game, (0, winHeight - 100), text = "Continue", center = True, colors = (colors.yellow, colors.white))
    toMainMenuButton.rect.centerx = winWidth / 2
    loadingScreenBGSurface = pygame.image.load(asset("loading screen.jpeg")).convert_alpha()
    loadingScreenBGSurface.fill((50, 50, 50), loadingScreenBGSurface.get_rect(), special_flags=pygame.BLEND_RGBA_MIN)
    if loadingScreenOn:
        loadingText = []
        tti = 0
        ti = 1
        for t in LOADING_TEXT:
            loadingText.append(Text(
                "2",
                t,
                colors.orangeRed,
                game.antialiasing,
                (10, 10 * ti)
            ))
            loadingText[tti].rect.centerx = winWidth / 2
            ti += 4
            tti += 1
        loadingLinesShowed = 1
        loadingLinesTimings = [0.05, 0.1, 0.017, 0.015, 0.015, 0.015, 0.015]
        tmmbt = "Skip"
        if not lssb:
            tmmbt = "Continue"
        toMainMenuButton = Button(game, (0, winHeight - 100), text = tmmbt, center = True, colors = (colors.yellow, colors.white))
        toMainMenuButton.rect.centerx = winWidth / 2
    else:
        toMainMenuButton.clicked = True

    print(colors.rgba(colors.yellow, 0))
    startButton = Button(game, (0, 340), text="Start", center = True, colors = (colors.rgba(colors.yellow, 255), colors.white), wh=(300, 60), rounded = True)
    settingsButton = Button(game, (0, 580), text="Settings", center=True, colors = (colors.yellow, colors.white))
    instructionsButton = Button(game, (0, 460), text="Instructions", center=True, colors = (colors.yellow, colors.white), wh=(250, 60))
    creditsButton = Button(game, (200, 580), text="Credits", center = True, colors = (colors.yellow, colors.white))

    settingsButton.rect.centerx = (winWidth / 2) - (settingsButton.rect.width / 2) - 10
    creditsButton.rect.centerx = (winWidth / 2) + (creditsButton.rect.width / 2) + 10

    comps = pygame.sprite.Group(startButton, instructionsButton) # Stands for components fyi
    for c in comps:
        c.rect.centerx = winWidth/2
    swordImg = pygame.transform.scale(pygame.image.load(asset('player/sw1.png')), (256, 256))
    swordRect = pygame.Rect(0, 130, swordImg.get_width(), swordImg.get_height())
    swordRect.centerx = winWidth/2
    text1 = Text('subtitle1', 'Press S to Start', colors.orangeRed, game.antialiasing,(30, 30))
    # text2 = Text('main-title1', TITLE, colors.orangeRed, game.antialiasing, (0, 30))
    title = pygame.image.load(asset("objects/TheCaverns2.png"))
    title.set_colorkey((255,255,255))
    titleRect = pygame.Rect(0, -80, title.get_width(), title.get_height())
    titleRect.centerx = winWidth/2
    #text3 = Text('title2', 'Created by LGgameLAB (with help)', colors.orangeRed, game.antialiasing, (0, 110))
    #text3.rect.centerx = winWidth/2

    #tv = 0
    while True:
        game.clock.tick(FPS)
        #pygame.time.delay(50)

        game.runEvents()
        #tv += 255 / loadingCounter
        #pygame.draw.rect(
        #    loadingScreenBGSurface,
        #    (0, 0, 0, tv),
        #    (0, 0, winWidth, winHeight)
        #)
        game.refresh(loadingScreenBGSurface)
        
        comps.update()
        creditsButton.update()
        settingsButton.update()

        iloadingLinesEloadingTextLen = int(loadingLinesShowed) == len(loadingText)
        keys = pygame.key.get_pressed()
        if keys[keySet['start']]:
            toMainMenuButton.clicked = True
 
        if toMainMenuButton.clicked:
            for comp in comps:
                game.win.blit(comp.image, comp.rect)
            game.win.blit(creditsButton.image, creditsButton.rect)
            game.win.blit(settingsButton.image, settingsButton.rect)

            if startButton.clicked:
                game.map.loadFloor()
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
        
            game.win.blit(text1.image, text1)
            game.win.blit(title, titleRect)
            game.win.blit(swordImg, swordRect)

            keys = pygame.key.get_pressed()

            if keys[keySet['start']]:
                game.map.loadFloor() 
                break
        else:

            for i in range(int(loadingLinesShowed)):
                game.win.blit(loadingText[i].image, loadingText[i])
            if loadingLinesShowed <= len(loadingText):
                loadingLinesShowed += loadingLinesTimings[int(loadingLinesShowed)] #0.05
            toMainMenuButton.update()
            if iloadingLinesEloadingTextLen or lssb:
                if toMainMenuButton.text != "Continue" and iloadingLinesEloadingTextLen:
                    toMainMenuButton.setText("Continue")
            game.win.blit(toMainMenuButton.image, toMainMenuButton.rect)
            #for t in loadingText:
            #    game.win.blit(t.image, t)
        
        pygame.display.update()

def gameOver(game):
    restartButton = Button(game, (winWidth/2, winHeight/2), text="Back to Menu", center = True, colors = (colors.yellow, colors.white))
    buttons = pygame.sprite.Group(restartButton)
    while True:
        game.clock.tick(FPS)
        
        game.runEvents()
        game.refresh()

        buttons.update()
        for btn in buttons:
            game.win.blit(btn.image, btn.rect)

        if restartButton.clicked:
            game.reset()
            break
        
        
        text1 = fonts['gameover'].render('Game Over', game.antialiasing, colors.dark(colors.red, 20))
        text2 = fonts['title1'].render("Score: " + str(game.points), game.antialiasing, (colors.yellow))
        
        game.win.blit(text1, (50,50))
        game.win.blit(text2, (800, 70))
        
        pygame.display.update()

def victoryLoop(game):
    menuButton = Button(game, (winWidth/2, winHeight/2), text="Back to Menu", center = True, colors = (colors.yellow, colors.white))
    buttons = pygame.sprite.Group(menuButton)
    game.mixer.playFx('yay')
    while True:
        game.clock.tick(FPS)
        
        game.runEvents()
        game.refresh()

        buttons.update()
        for btn in buttons:
            game.win.blit(btn.image, btn.rect)

        if menuButton.clicked:
            game.reset()
            break
        
        text1 = fonts['victory'].render('Victory', game.antialiasing, colors.yellow, 20)
        text2 = fonts['title1'].render("Score: " + str(game.points), game.antialiasing, (colors.yellow))
        
        game.win.blit(text2, (800, 70))
        game.win.blit(text1, (winWidth/2 - text1.get_width()/2 ,30))
        
        pygame.display.update()
