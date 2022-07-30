from .screen import Screen

class GameScreen(Screen):
    def __init__(self, manager):
        Screen.__init__(self, manager)
    def update(self):
        """Update the screen"""
        self.surface.fill(
            self.manager.game.settings.backgroundColor
        )
        if self.activeMenu != None:
            self.menus[self.activeMenu].update()
    def clickAt(self, cpos):
        """Responds to a click at cpos
        
        Arguments:
        -----
        cpos: tuple
            The click position (x, y)
        """