import pygame
import fx
import pygame
from animations import *
from stgs import *
import util

class Npc1(util.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.groups =  game.sprites, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.imgSrc = pygame.image.load(asset("objects/npc1.png"))
        self.image = self.imgSrc.copy()
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.center = objT.x, objT.y
        self.pos = pygame.Vector2((self.rect.x, self.rect.y))
        self.player = self.game.player
        self.angle = -40
        self.text = 'LMFAO'
        self.setAngle()
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v
    
    def update(self):
        # self.setAngle()
        self.checkInteract()
        self.move()
    
    def move(self):
        self.pos.update(self.rect.x, self.rect.y)
        # pDir = pygame.Vector2(self.game.player.rect.center)
        # diff = pygame.Vector2(pDir.x-self.pos.x, pDir.y-self.pos.y).normalize()
        # if not self.angle == pDir:
        #     self.angle = math.degrees(math.atan2(-diff.y, diff.x))
        #     self.setAngle()

    def checkInteract(self):
        if checkKey('interact') and pygame.time.get_ticks()-self.game.dialogueScreen.lastInteract > 240:
            iRect = pygame.Rect(0, 0, 50, 50)
            iRect.center = self.rect.center
            if iRect.colliderect(self.player.rect):
                Vec = pygame.Vector2(self.player.rect.centerx-self.rect.centerx, self.player.rect.centery-self.rect.centery).normalize()
                try:
                    self.angle = math.degrees(math.atan2(-Vec.y, Vec.x))
                except ValueError:
                    self.angle = 0
                self.setAngle()
                self.game.dialogueScreen.dialogue(self)

    def setAngle(self):
        self.rotCenter()

    def getCollider(self):
        collideRect = pygame.Rect(0, 0, 20, 20)
        collideRect.center = self.rect.center
        return collideRect

    def rotCenter(self, angle=False):
        if not angle:
            angle = self.angle
        self.image = pygame.transform.rotate(self.imgSrc, angle-90)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)
        self.mask = pygame.mask.from_surface(self.image, True)
