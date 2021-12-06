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
        
        text1 = fonts['title1'].render(TITLE, game.antialiasing, colors.yellow)
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
    fpsButton = Button(game, (800, 250), text = 'Toggle FPS',  colors=(colors.yellow, colors.white),  onClick = lambda:game.toggleFps() ,groups = [comps], center = True)
    aaliasButton = Button(game, (800, 330), text = 'Toggle Anti - Aliasing', onClick = lambda:game.toggleAalias() ,groups = [comps], center = True, colors=(colors.yellow, colors.white))
    joystickButton = Button(game, (800, 530), text = 'Joystick Disable', onClick = game.disableJoystick ,groups = [comps], center = True, colors=(colors.yellow, colors.white))
    texts = [
        Text('title2', 'Paused', colors.orangeRed, game.antialiasing, (winWidth/2.4, 10)),
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
        
        text2 = fonts['title1'].render(TITLE, game.antialiasing, colors.orangeRed)
        game.win.blit(text2, (30,30))

        keys = pygame.key.get_pressed()
        
        pygame.display.update()

def main(game):
    startButton = Button(game, (winWidth/2 + 140, 140), text="Start", center = True, colors = (colors.yellow, colors.white))
    stgsButton = Button(game, (winWidth/2 + 140, 380), text="Settings", center=True, colors = (colors.yellow, colors.white))
    compendButton = Button(game, (winWidth/2 + 140, 260), text="Game Instructions", center=True, colors = (colors.yellow, colors.white))
    comps = pygame.sprite.Group(startButton, stgsButton, compendButton) # Stands for components fyi
    swordImg = pygame.image.load(asset('player/sw1.png'))
    while True:
        pygame.time.delay(50)
        
        game.runEvents()
        game.refresh()

        comps.update()
        for comp in comps:
            game.win.blit(comp.image, comp.rect)

        if startButton.clicked:
            game.map.loadLevel()
            break
        
        if stgsButton.clicked:
            settingsMenu(game)
            stgsButton.reset()
        
        if compendButton.clicked:
            compendiumMenu(game)
            compendButton.reset()
        
        text1 = game.font2.render('Press S to Start', game.antialiasing, colors.orangeRed)
        text2 = game.font1.render(TITLE, game.antialiasing, colors.orangeRed)
        text3 = game.font1.render('Created by GameLAB', game.antialiasing, colors.orangeRed)
        
        game.win.blit(text1, (30,30))
        game.win.blit(text2, (100, 200))
        game.win.blit(text3, (100, 300))

        game.win.blit(pygame.transform.scale(swordImg, (320, 320)), (100, 300))

        keys = pygame.key.get_pressed()

        if keys[keySet['start']]:
            game.map.loadLevel()
            break
        
        pygame.display.update()

def gameOver(game):
    restartButton = Button(game, (winWidth/2, winHeight/2), text="Back to Menu", center = True, colors = (colors.yellow, colors.white))
    buttons = pygame.sprite.Group(restartButton)
    while True:
        pygame.time.delay(50)
        
        game.runEvents()
        game.refresh()

        buttons.update()
        for btn in buttons:
            game.win.blit(btn.image, btn.rect)

        if restartButton.clicked:
            game.reset()
            break
        
        
        text1 = game.gameOverFont.render('Game Over', game.antialiasing, colors.dark(colors.red, 20))
        text2 = fonts['title1'].render("Score: " + str(game.points), game.antialiasing, (colors.yellow))
        
        game.win.blit(text1, (50,50))
        game.win.blit(text2, (800, 70))
        
        pygame.display.update()

def victoryLoop(game):
    menuButton = Button(game, (winWidth/2, winHeight/2), text="Back to Menu", center = True, colors = (colors.yellow, colors.white))
    buttons = pygame.sprite.Group(menuButton)
    game.mixer.playFx('yay')
    while True:
        pygame.time.delay(50)
        
        game.runEvents()
        game.refresh()

        buttons.update()
        for btn in buttons:
            game.win.blit(btn.image, btn.rect)

        if menuButton.clicked:
            game.reset()
            break
        
        text1 = game.victoryFont.render('Victory', game.antialiasing, colors.yellow, 20)
        text2 = fonts['title1'].render("Score: " + str(game.points), game.antialiasing, (colors.yellow))
        
        game.win.blit(text2, (800, 70))
        game.win.blit(text1, (winWidth/2 - text1.get_width()/2 ,30))
        
        pygame.display.update()