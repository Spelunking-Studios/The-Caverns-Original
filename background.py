import pygame

class Background:
    def __init__(self, bgColor = (0, 0, 0)):
        self.isBgImage = False
        self.bgFile = None
        self.bgColor = bgColor
    def setBGImage(self, fp):
        self.bgFile = fp
    def setBGColor(self, color):
        self.bgColor = color
    def draw(self, surface):
        if self.isBgImage:
            pass
        else:
            pygame.draw.rect(surface, self.bgColor, surface.get_rect())