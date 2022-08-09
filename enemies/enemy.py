import pygame

class Enemy():
    """Base Enemy class"""
    def __init__(self, room, objT):
        self.room = room
        self.objT = objT
        self.rect = pygame.Rect(objT.x, objT.y, 20, 20)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill((0, 255, 0))
        self.origImage = self.image.copy()
    def setPos(self, pos):
        """Set the position of the enemy
        
        Arguments:
        -----
        pos: tuple
            The position (x, y)
        """
        pass