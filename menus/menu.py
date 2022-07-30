from pygame.sprite import Group

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