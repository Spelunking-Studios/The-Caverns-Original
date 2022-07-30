class ScreenManager:
    """Manages multiple screens for the game"""
    def __init__(self, game):
        """Initializes the screen
        
        Arguments:
        -----
        game: Game
            The game
        """
        self.screens = []
        self.game = game
    def addScreen(self, screen):
        """Adds a screen to the screen manager"""
        self.screens.append(screen)
    def setScreen(self, index):
        """Sets the currently active screen"""
        self.activeScreen = self.screens[index]