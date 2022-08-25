# import pygame, math

# class NavigEnt(pygame.sprite.Sprite):
#     def __init__(self, room, objT):
#         pygame.sprite.Sprite.__init__(self)
#         self.room = room
#         self.objT = objT
#         self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
#         self.normalRect = self.rect.copy()
#         self.rot = self.objT.rotation
#         self.updateRot()
#         print(self.rect, self.normalRect)
            
#     def updateRot(self):
#         if self.rot != 0:
#             print(self.objT.rotation)
#             angle = -self.objT.rotation
#             # Make a image and rotate that, and get the rect
#             # Thnks pygame for doing the math for me ;)
#             rrsurf = pygame.Surface(self.normalRect[2:])
#             pygame.transform.rotate(rrsurf, angle)
#             self.rect = rrsurf.get_rect()
#             self.rect.x = self.normalRect[0]
#             self.rect.y = self.normalRect[1]

# class Entrance(NavigEnt):
#     def __init__(self, room, objT):
#         NavigEnt.__init__(self, room, objT)

# class Exit(NavigEnt):
#     def __init__(self, room, objT):
#         NavigEnt.__init__(self, room, objT)