import pygame
from src.shaders import ShaderPass
from src.stgs import *

class Display:

    def __init__(self):
        self.resolution = pygame.display.list_modes()[0]
        # self.display = pygame.display.set_mode(self.resolution)
        self.display = pygame.display.set_mode((winWidth, winHeight), winFlags)
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(pygame.image.load(iconPath))
        self.display.convert(32, pygame.RLEACCEL) 

    def getFullScreen(self):
        keys = pygame.key.get_pressed()
        if keys[keySet['fullScreen']]:
            if self.fullScreen:
                self.display = pygame.display.set_mode((winWidth, winHeight), winFlags)
                self.fullScreen = False
            else:
                self.display = pygame.display.set_mode((winWidth, winHeight), winFlags | pygame.FULLSCREEN)
                self.fullScreen = True
            pygame.display.set_icon(pygame.image.load(iconPath))
            #pygame.display.toggle_fullscreen()
    
    def update(self, window):
        self.getFullScreen()

        self.display.blit(window, (0, 0))
        pygame.display.update()
    
    # Blit passthrough
    def blit(self, img, rect):
        self.display.blit(img, rect)
