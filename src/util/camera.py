import pygame
from src.stgs import *

class Cam:

    def __init__(self, game, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.limit = CAMLIMIT
        self.game = game
        self.target = game.player

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def applyRect(self, rect):
        return rect.move(self.camera.topleft)

    def applyVec(self, vec):
        return vec + self.camera.topleft

    def toggleTarget(self):
        if self.target == self.game.player:
            self.target = self.game.level.door
        else:
            self.target = self.game.player
        
    def update(self):
        self.width, self.height = self.game.map.floor.room.width, self.game.map.floor.room.height
        x = -self.target.rect.centerx + int(winWidth / 2)
        y = -self.target.rect.centery + int(winHeight / 2)

        # limit scrolling to map size
        if self.limit:
            x = min(0, x)  # left
            y = min(0, y)  # top
            x = max(-(self.width - winWidth), x)  # right
            y = max(-(self.height - winHeight), y)  # bottom
        
        if self.width < winWidth:
            x = (winWidth/2 - self.width/2)
        if self.height < winHeight:
            y = (winHeight/2 - self.height/2)

        self.camera = pygame.Rect(x, y, self.width, self.height)
