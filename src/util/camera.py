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

    def applyTuple(self, tup):
        return tup[0] + self.camera.topleft[0], tup[1] + self.camera.topleft[1]

    def toggleTarget(self):
        if self.target == self.game.player:
            self.target = self.game.level.door
        else:
            self.target = self.game.player
        
    def update(self):
        self.width, self.height = self.game.map.floor.room.width, self.game.map.floor.room.height
        x = -self.target.rect.centerx + int(self.game.width() / 2)
        y = -self.target.rect.centery + int(self.game.height() / 2)

        # limit scrolling to map size
        if self.limit:
            x = min(0, x)  # left
            y = min(0, y)  # top
            x = max(-(self.width - self.game.width()), x)  # right
            y = max(-(self.height - self.game.height()), y)  # bottom
        
        if self.width < self.game.width():
            x = (self.game.width()/2 - self.width/2)
        if self.height < self.game.height():
            y = (self.game.height()/2 - self.height/2)

        self.camera = pygame.Rect(x, y, self.width, self.height)
