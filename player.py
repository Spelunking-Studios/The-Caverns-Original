from entity import Entity
import pygame, os, math

class Player(Entity):
    """Represents a player"""
    def __init__(self, map, pos = (0, 0), size = (64, 64)):
        """Initialize the player"""
        Entity.__init__(self, map, pos, size)
        self.imagePath = self.map.level.game.asset(
            os.path.join("player", "samplePlayer.png")
        )
        self.surface = pygame.image.load(self.imagePath)
        self.image = self.surface.copy()
    def update(self):
        """Update the player"""
        self.surface = pygame.transform.rotate(
            self.image,
            self.getAngle()
        )
        self.surface = pygame.transform.scale(
            self.surface,
            (self.width, self.height)
        )
    def getAngle(self):
        """Gets the angle (in degrees) between the mouse and the player
        
        For Devs:
        -----
        See devStuff/"the mouse and player triangle math.jpg" 
        """
        m = self.map.level.game.mousePos
        p = [
            self.map.level.game.settings.windowSize[0] / 2 + (self.width / 2),
            self.map.level.game.settings.windowSize[1] / 2 + (self.height / 2)
        ]
        
        r = pygame.math.Vector2(m) - pygame.math.Vector2(p)
        rad, angle = r.as_polar()
        return -(angle + 90)
    def draw(self):
        """Draw the player"""
        Entity.draw(self)