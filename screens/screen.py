import pygame

class Screen:
    """Represents one screen"""
    def __init__(self, manager):
        """Initializes the screen
        
        Arguments:
        -----
        manager: ScreenManager
            The screen manager
        """
        self.manager = manager
        self.surface = (
            pygame.Surface(self.manager.game.settings.windowSize)
        ).convert_alpha()
        self.menus = []
        self.activeMenu = None
    def update(self):
        """Update the screen"""
        self.surface.fill(
            self.manager.game.settings.backgroundColor
        )
        if self.activeMenu != None:
            self.menus[self.activeMenu].update()
    def addMenu(self, menu):
        """Adds a menu
        
        Arguments:
        -----
        menu: Menu
        """
        self.menus.append(menu)
    def setActiveMenu(self, index):
        """Set the active menu"""
        self.activeMenu = index
    def clickAt(self, cpos):
        """Responds to a click at cpos
        
        Arguments:
        -----
        cpos: tuple
            The click position (x, y)
        """
        # Pass click to menu
        self.menus[self.activeMenu].clickAt(cpos)