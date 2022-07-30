import pygame, sys, os
from settings import Settings
from background import Background
from screens import ScreenManager, Screen
from menus import Menu, Button, Text

# Init pygame
pygame.init()

# Get the top level path
try:
    path = sys._MEIPASS
except AttributeError:
    path = os.path.dirname(os.path.realpath(__file__))

class Game:
    """Represents the game"""
    def __init__(self):
        """Initializes the game"""
        # Events
        self.events = []
        # Cooldowns
        self.mouseClickCooldown = 0
        # Create a settings object to manage the game settings
        self.settings = Settings()
        # Background
        self.background = Background()
        self.background.setBGColor(self.settings.backgroundColor)
        # Create the window and set it up
        self.window = pygame.display.set_mode(self.settings.windowSize, pygame.SWSURFACE)
        pygame.display.set_caption(self.settings.title)
        # Create game clock
        self.clock = pygame.time.Clock()
        # FPS
        self.fps = 0
        # Setup Screens
        self.screenManager = ScreenManager(self)
        self.screenManager.addScreen(Screen(self.screenManager))
        self.screenManager.setScreen(0)
        # Setup Menus
        # Main menu
        self.screenManager.activeScreen.addMenu(
            Menu(self.screenManager.activeScreen)
        )
        self.screenManager.activeScreen.setActiveMenu(0)
        self.screenManager.activeScreen.menus[0].addMenuItem(
            Text(
                self.screenManager.activeScreen.menus[0],
                pos = (600, 150),
                size = (200, 50),
                text = self.settings.title,
                color = (255, 255, 0),
                fontSize = 60,
                centered = [True, False]
            )
        )
        self.screenManager.activeScreen.menus[0].addMenuItem(
            Button(
                self.screenManager.activeScreen.menus[0],
                pos = (500, 350),
                size = (200, 50),
                text = "Play",
                color = (255, 255, 0),
                fontSize = 20
            )
        )
        self.screenManager.activeScreen.menus[0].addMenuItem(
            Button(
                self.screenManager.activeScreen.menus[0],
                pos = (500, 410),
                size = (200, 50),
                text = "Settings",
                color = (255, 255, 0),
                fontSize = 20
            )
        )
        self.screenManager.activeScreen.menus[0].addMenuItem(
            Button(
                self.screenManager.activeScreen.menus[0],
                pos = (500, 470),
                size = (200, 50),
                text = "Quit",
                color = (255, 255, 0),
                fontSize = 20
            )
        )
    def run(self):
        """Runs the game"""
        while True:
            # Slows framespeed down to or below the ideal fps
            self.clock.tick(self.settings.idealFPS)
            self.updateFPS()
            self.addPygameEvents()
            # Handle Events
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.quit()
                if self.mouseClickCooldown > 0:
                    self.mouseClickCooldown -= self.clock.get_time()
                if self.mouseClickCooldown <= 0:
                    mouseVals = pygame.mouse.get_pressed()
                    if mouseVals[0]:
                        print(f"Click at {pygame.mouse.get_pos()}")
                        self.mouseClickCooldown = self.settings.mouseClickCooldown
            # Draw background
            self.background.draw(self.window)
            # Update the active screen
            self.screenManager.activeScreen.update()
            # Draw the active screen
            self.window.blit(
                self.screenManager.activeScreen.surface,
                self.screenManager.activeScreen.surface.get_rect()
            )
            # Update the display
            pygame.display.update()
    def quit(self):
        """Quits the game"""
        print("Quitting...")
        pygame.quit()
        sys.exit()
    def addPygameEvents(self):
        """Adds pygame's events to the game's events list"""
        for event in pygame.event.get():
            self.events.append(event)
    def updateFPS(self):
        """Updates the FPS variable"""
        self.fps = self.clock.get_fps()
    # Asset Stuff - Just call root asset module functions
    def asset(self, fn):
        """Returns the path to a given asset"""
        global path
        return os.path.join(path, "assets", fn)
    def fasset(self, fn):
        """Returns the path to a given asset"""
        global path
        return os.path.join(path, "fonts", fn)