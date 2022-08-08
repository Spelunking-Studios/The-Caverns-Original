import pygame, math

class NavigEnt(pygame.sprite.Sprite):
    def __init__(self, room, objT):
        pygame.sprite.Sprite.__init__(self)
        self.room = room
        self.objT = objT
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        # Rotation
        if self.objT.rotation != 0:
            print(self.objT.rotation)
            angle = math.radians(-self.objT.rotation)
            print(math.degrees(angle))
            #cx = self.objT.centerX
            #cy = self.objT.centerY

class Entrance(NavigEnt):
    def __init__(self, room, objT):
        NavigEnt.__init__(self, room, objT)

class Exit(NavigEnt):
    def __init__(self, room, objT):
        NavigEnt.__init__(self, room, objT)