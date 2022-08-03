import pygame
from overlay import *
from menu import *
from stgs import *
import colors

def compendiumMenu(game):
    x, y = 100, 100
    stepX, stepY = 180, 120
    returnButton = Button(game, (winWidth-240, 70), text="Return", center = True)
    #MenuItem(game, (x, y), asset(''), desc='', text=''),
    itemCompendium = [
        MenuItem(game, (x, y), asset('player/sw1.png'), zoomMin = 1.5, zoomMax = 2.8, desc='You take on the role of a brave sword who dares to save his kingdom from terrorizing monsters. The sword represents your being and your weapon joined together as one. Use yourself wisely', text='Sword'),
        MenuItem(game, (x+stepX, y), asset('objects/redPole.png'), zoomMax = 1.5, desc="This game uses the mouse to direct yourgame (The sword if you haven't gotten that) and upon a click you will be launched in the direction of its pointer. To advance to each level, the player must reach the stone pole bearing the red magic AFTER DEFEATING ALL THE MONSTERS! Press C to toggle the camera between the end post view and the player view. Also press R to restart an attempt on a level and P to pause. Good luck on your journey!", text='Know ur 101s'),
        MenuItem(game, (x+stepX*2, y), asset('objects/greenPole.png'), zoomMax = 1.5, desc='This rebounder pole shows up with a green magical aura. This represents your only means of changing direction in this game. Make sure you you aim yourself well ;)', text='Rebounder pole'),
    ]
    comps = pygame.sprite.Group(returnButton,) #itemCompendium)
    descText = ''
    while True:
        descText = ''
        pygame.time.delay(50)
        
        game.runEvents()
        game.refresh()

        comps.update()
        for comp in comps:
            game.win.blit(comp.image, comp.rect)

        # for i in itemCompendium:
        #     if i.hover:
        #         descText = i.desc

        if returnButton.clicked:
            break

        if checkKey(keySet['start']):
            game.map.loadLevel()
            break
        
        text1 = fonts['main-title1'].render(TITLE, game.antialiasing, colors.yellow)
        text2 = Text('description1', descText, colors.yellow, game.antialiasing, (winWidth- 1200,winHeight - 340), True)
        game.win.blit(text1, (30,winHeight - 70))
        game.win.blit(text2.image, text2.pos)

        keys = pygame.key.get_pressed()
        
        pygame.display.update()

def settingsMenu(game):
    returnButton = Button(game, (winWidth-240, 70), text="Return", center = True, colors=(colors.yellow, colors.white))
    comps = pygame.sprite.Group(returnButton)
    audioSlider1 = SettingSlider(game, (100, 350), addGroups = [comps])
    audioSlider2 = SettingSlider(game, (100, 500), addGroups = [comps])
    audioSlider1.image.set_colorkey((0,0,0))
    audioSlider2.image.set_colorkey((0,0,0))
    fpsButton = Button(game, (800, 250), text = 'Toggle FPS',  colors=(colors.yellow, colors.white),  onClick = game.toggleFps ,groups = [comps], center = True)
    aaliasButton = Button(game, (800, 330), text = 'Toggle Anti - Aliasing', onClick = game.toggleAalias ,groups = [comps], center = True, colors=(colors.yellow, colors.white))
    joystickButton = Button(game, (800, 530), text = 'Joystick Disable', onClick = game.disableJoystick ,groups = [comps], center = True, colors=(colors.yellow, colors.white))
    texts = [
        Text('title1', 'Audio Control', colors.orangeRed, game.antialiasing, (75, 250)),
        Text('caption1', 'Music Volume', colors.orangeRed, game.antialiasing, (75, 325)),
        Text('caption1', 'Fx Volume', colors.orangeRed, game.antialiasing, (75, 475))
    ]
    def applyComps():
        game.mixer.setMusicVolume(audioSlider1.get_ratio())
        game.mixer.setFxVolume(audioSlider2.get_ratio())

    audioSlider1.setRatio(game.mixer.musicVolume)
    audioSlider2.setRatio(game.mixer.fxVolume)

    while True:
        pygame.time.delay(50)
        
        game.runEvents()
        game.refresh()
        applyComps()

        comps.update()
        for comp in comps:
            game.win.blit(comp.image, comp.rect)

        for t in texts:
            game.win.blit(t.image, t.rect)

        if returnButton.clicked:
            break

        if checkKey(keySet['start']):
            game.map.loadLevel()
            break
        
        text2 = fonts['main-title1'].render(TITLE, game.antialiasing, colors.orangeRed)
        game.win.blit(text2, (30,30))

        keys = pygame.key.get_pressed()
        
        pygame.display.update()

def main(game, loadingScreenOn = False):
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
        toMainMenuButton = Button(game, (0, winHeight - 100), text = "Continue", center = True, colors = (colors.yellow, colors.white))
        toMainMenuButton.rect.centerx = winWidth / 2
    else:
        toMainMenuButton.clicked = True

    startButton = Button(game, (0, 340), text="Start", center = True, colors = (colors.yellow, colors.white), wh=(300, 60))
    settingsButton = Button(game, (0, 580), text="Settings", center=True, colors = (colors.yellow, colors.white))
    instructionsButton = Button(game, (0, 460), text="Instructions", center=True, colors = (colors.yellow, colors.white), wh=(250, 60))
    creditsButton = Button(game, (200, 580), text="Credits", center = True, colors = (colors.yellow, colors.white))

    settingsButton.rect.centerx = (winWidth / 2) - (settingsButton.rect.width / 2) - 10
    creditsButton.rect.centerx = (winWidth / 2) + (creditsButton.rect.width / 2) + 10

    comps = pygame.sprite.Group(startButton, instructionsButton) # Stands for components fyi
    for c in comps:
        c.rect.centerx = winWidth/2
    swordImg = pygame.transform.scale(pygame.image.load(asset('player/sw1.png')), (320, 320))
    swordRect = pygame.Rect(0, 65, swordImg.get_width(), swordImg.get_height())
    swordRect.centerx = winWidth/2
    text1 = Text('subtitle1', 'Press S to Start', colors.orangeRed, game.antialiasing,(30, 30))
    text2 = Text('main-title1', TITLE, colors.orangeRed, game.antialiasing, (0, 30))
    text2.rect.centerx = winWidth/2
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
        game.refresh(bg = loadingScreenBGSurface, isSurface = True)
        
        comps.update()
        creditsButton.update()
        settingsButton.update()

        if toMainMenuButton.clicked:
            for comp in comps:
                game.win.blit(comp.image, comp.rect)
            game.win.blit(creditsButton.image, creditsButton.rect)
            game.win.blit(settingsButton.image, settingsButton.rect)

            if startButton.clicked:
                game.map.loadLevel()
                break
            
            if settingsButton.clicked:
                settingsMenu(game)
                settingsButton.reset()
            
            if instructionsButton.clicked:
                compendiumMenu(game)
                instructionsButton.reset()
            
            if creditsButton.clicked:
                creditsMenu(game)
                creditsButton.reset()
        
            game.win.blit(text1.image, text1)
            game.win.blit(text2.image, text2)
            game.win.blit(swordImg, swordRect)

            keys = pygame.key.get_pressed()

            if keys[keySet['start']]:
                game.map.loadLevel()
                break
        else:
            for i in range(int(loadingLinesShowed)):
                game.win.blit(loadingText[i].image, loadingText[i])
            if loadingLinesShowed <= len(loadingText):
                loadingLinesShowed += loadingLinesTimings[int(loadingLinesShowed)] #0.05
            toMainMenuButton.update()
            if int(loadingLinesShowed) == len(loadingText):
                game.win.blit(toMainMenuButton.image, toMainMenuButton.rect)
            #for t in loadingText:
            #    game.win.blit(t.image, t)
        
        pygame.display.update()

def creditsMenu(game):
    loadingScreenBGSurface = pygame.image.load(asset("loading screen.jpeg")).convert_alpha()
    loadingScreenBGSurface.fill((50, 50, 50), loadingScreenBGSurface.get_rect(), special_flags=pygame.BLEND_RGBA_MIN)
    title = Text("title1", "Credits", colors.orangeRed, game.antialiasing, (0, 50))
    gfxTitle = Text("subtitle1", "~~~ Graphics ~~~", colors.orangeRed, game.antialiasing, (0, 150))
    gfxName1 = Text("3", "Matthew Hosier", colors.orangeRed, game.antialiasing, (0, 225))
    codeTitle = Text("subtitle1", "~~~ Code ~~~", colors.orangeRed, game.antialiasing, (0, 275))
    codeName1 = Text("3", "Luke Gonsalves", colors.orangeRed, game.antialiasing, (0, 350))
    codeName2 = Text("3", "Ben Landon", colors.orangeRed, game.antialiasing, (0, 425))
    menuItems = [title, gfxTitle, gfxName1, codeTitle, codeName1, codeName2]
    # Pre-calculate half of the windows width because division is slow
    halfWinWidth = winWidth / 2
    for item in menuItems:
        item.rect.centerx = halfWinWidth
    while True:
        game.clock.tick(FPS)
        game.runEvents()
        game.refresh(bg = loadingScreenBGSurface, isSurface = True)
        for item in menuItems:
            game.win.blit(item.image, item.rect)
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