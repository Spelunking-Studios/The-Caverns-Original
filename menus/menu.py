from pygame.sprite import Group
from .button import Button

class Menu:
    """A menu"""
    def __init__(self, screen):
        """Initialize the menu
        
        Arguments:
        -----
        screen: Screen
        """
        self.screen = screen
        # Group of menu items
        self.menuItems = Group()
    def addMenuItem(self, menuItem):
        """Add a menu item
        
        Arguments:
        -----
        menuItem: MenuItem
        """
        self.menuItems.add(menuItem)
    def update(self):
        "Update the menu"
        self.menuItems.update()
    def clickAt(self, cpos):
        """Responds to a click at cpos
        
        Arguments:
        -----
        cpos: tuple
            The click position (x, y)
        """
        # Check if the click hits any menu items
        for menuItem in list(self.menuItems):
            # Check to see if menuItem is a button
            if isinstance(menuItem, Button):
                # Use pygame.Rect.collidepoint because buttons are rectuangular
                if menuItem.getRect().collidepoint(cpos):
                    menuItem.triggerEvent("click")