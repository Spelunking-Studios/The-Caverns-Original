import pygame
from pygame.sprite import Sprite

class MenuItem(Sprite):
    """Base class for all menu items. Do not actually use this class"""
    def __init__(self, menu, pos = (0, 0), size = (200, 100), color = (255, 255, 255)):
        """Initialize the menu item
        
        Arguments:
        -----
        menu: Menu
        pos: tuple = (0, 0)
            The position (x, y) of the menu item.
        size: tuple = (200, 100)
            The size (width, height) of the menu item.
        """
        Sprite.__init__(self)
        self.menu = menu
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.handlers = []
        self.events = []
        self.color = color
    def update(self):
        self.draw()
    def draw(self):
        pygame.draw.rect(self.menu.screen.surface, self.color, self.getRect())
    def addHandler(self, handler, type):
        self.handlers.append({
            "eType": type,
            "handler": handler
        })
    def triggerEvent(self, eType):
        """Triggers an event of type eType
        
        Arguments:
        -----
        eType: string
            The event type
        """
        for handler in self.handlers:
            if handler["eType"] == eType:
                handler["handler"]({})
    def getRect(self):
        return pygame.Rect(
            self.x, self.y,
            self.width, self.height
        )