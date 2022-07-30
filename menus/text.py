from .menuItem import MenuItem
from pygame.font import Font
import pygame

class Text(MenuItem):
    def __init__(self, menu, pos = (0, 0), size = (200, 100), text = "",
        color = (255, 255, 255), fontColor = (0, 0, 0), fontSize = 15,
        centered = [False, False]):
        """Initialize text
        
        Arguments:
        -----
        menu: Menu
        pos: tuple = (0, 0)
            The position (x, y) of the text
        size: tuple = (200, 100)
            The size (width, height) of the text
        text: string = ""
        color: tuple = (255, 255, 255)
            The color (r, g, b) of the text
        fontSize: int = 15
            The font size
        centered: [boolean, boolean] = [False, False]
            Is the text centered? Positon 0 is for x axis centering.
            Position 1 is for y axis centering.
        """
        MenuItem.__init__(self, menu, pos, size, color)
        self.text = text
        self.color = color
        self.fontSize = fontSize
        self.centered = centered
        self.fontFilePath = self.menu.screen.manager.game.fasset("YuseiMagic-Regular.ttf")
        self.font = Font(self.fontFilePath, self.fontSize)
        self.textSurface = self.font.render(self.text, False, self.color)
        self.rect = self.getRect()
    def getRect(self):
        # Generic rect
        rect = [self.x, self.y, self.width, self.height]
        # Centered rects
        # Get size of rendered text
        rsize = self.font.size(self.text)
        # X axis
        if self.centered[0]:
            rect[0] = rect[0] - (rsize[0] / 2)
        # Y axis
        if self.centered[1]:
            rect[1] = rect[1] - (rsize[1] / 2)
        rect = pygame.Rect(rect)
        return rect
    def draw(self):
        """Draw the text"""
        self.menu.screen.surface.blit(
            self.textSurface,
            self.rect
        )