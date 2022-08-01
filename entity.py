import pygame
from pygame.sprite import Sprite

class Entity(Sprite):
    """Represents an entity"""
    def __init__(self, map, pos = (0, 0), size = (32, 32)):
        """Initialize the entity
        
        Arguments:
        -----
        map: Map
            The map the entity is on
        pos: tuple = (0, 0)
            The position (x, y) of the entity
        size: tuple = (32, 32)
            The size (width, height) of the entity
        """
        Sprite.__init__(self)
        self.map = map
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))
    def update(self):
        """Update the entity"""
        pass
    def draw(self):
        """Draw the entity"""
        self.map.surface.blit(
            self.surface,
            (self.x * 32, self.y * 32)
        )
    def setPos(self, pos):
        """Sets the position of the entity
        
        Arguments:
        -----
        pos: tuple
            The position (x, y)
        """
        self.x = pos[0]
        self.y = pos[1]