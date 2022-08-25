import pygame
import colors
from menu import SettingSlider, Button, Text
from stgs import winWidth, winHeight

class PauseOverlay(pygame.sprite.Sprite):
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
            
        self.audioSlider1 = SettingSlider(self.game, (100, 350), addGroups = [self.components])
        self.audioSlider2 = SettingSlider(self.game, (100, 500), addGroups = [self.components])
        self.audioSlider1.image.set_colorkey((0,0,0))
        self.audioSlider2.image.set_colorkey((0,0,0))
        self.fpsButton = Button(self.game, (800, 250), text = 'Toggle FPS', onClick = self.game.toggleFps ,groups = [self.components], center = True, colors=(colors.yellow, colors.white))
        self.aaliasButton = Button(self.game, (800, 330), text = 'Toggle Anti - Aliasing', onClick = self.game.toggleAalias ,groups = [self.components], center = True, colors=(colors.yellow, colors.white))
        Button(self.game, (350, 550), groups = [self.components], text = "Return to menu", onClick=self.game.endgame, center = True, colors = (colors.yellow, colors.white))
    
        self.text = [
            Text('title2', 'Paused', colors.orangeRed, self.game.antialiasing, (self.rect.width/2.4, 10)),
            Text('title1', 'Audio Control', colors.orangeRed, self.game.antialiasing, (75, 250)),
            Text('caption1', 'Music Volume', colors.orangeRed, self.game.antialiasing, (75, 325)),
            Text('caption1', 'Fx Volume', colors.orangeRed, self.game.antialiasing, (75, 475))
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