import pygame

class NavigEnt(pygame.sprite.Sprite):
    def __init__(self, room, objT):
        pygame.sprite.Sprite.__init__(self)
        self.room = room
        self.objT = objT
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

class Entrance(NavigEnt):
    def __init__(self, room, objT):
        NavigEnt.__init__(self, room, objT)

class Exit(NavigEnt):
    def __init__(self, room, objT):
        NavigEnt.__init__(self, room, objT)