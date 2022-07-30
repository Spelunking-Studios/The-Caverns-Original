from .menuItem import MenuItem
from pygame.font import Font
import pygame

class Button(MenuItem):
    def __init__(self, menu, pos = (0, 0), size = (200, 100), text = "",
        color = (255, 255, 255), fontColor = (0, 0, 0), fontSize = 15):
        """Initialize the button
        
        Arguments:
        -----
        menu: Menu
        pos: tuple = (0, 0)
            The position (x, y) of the button
        size: tuple = (200, 100)
            The size (width, height) of the button
        text: string = ""
            The text in the button
        color: tuple = (255, 255, 255)
            The color (r, g, b) of the button
        fontColor: tuple = (0, 0, 0)
            The font color (r, g, b) of the button
        fontSize: int = 15
            The font size
        """
        MenuItem.__init__(self, menu, pos, size, color)
        self.text = text
        self.fontColor = fontColor
        self.fontSize = fontSize
        self.fontFilePath = self.menu.screen.manager.game.fasset("YuseiMagic-Regular.ttf")
        self.font = Font(self.fontFilePath, self.fontSize)
        self.textSurface = self.font.render(self.text, False, self.fontColor)
        self.textRect = self.getTextRect()
    def getTextRect(self):
        # Get the size of the text once it is rendered
        textSize = self.font.size(self.text)
        # Get a basic rect
        textRect = list(pygame.Rect(0, 0, textSize[0], textSize[1]))
        # If the text height is less than the button height
        # Center the text vertically in the button
        if textSize[1] < self.height:
            textRect[1] = ((self.height - textSize[1]) / 2) + self.y
        # If the text width is thess that the button width
        # Center the text horizontally in the butto
        if textSize[0] < self.width:
            textRect[0] = ((self.width - textSize[0]) / 2) + self.x
        textRect = pygame.Rect(textRect)
        return textRect
    def draw(self):
        """Draw the button"""
        pygame.draw.rect(self.menu.screen.surface, self.color, self.getRect())
        self.menu.screen.surface.blit(
            self.textSurface,
            self.textRect
        )
    def addClickHandler(self, handler):
        """Adds a click handler
        
        Arguments:
        -----
        handler: function
        """
        self.addHandler(handler, "click")