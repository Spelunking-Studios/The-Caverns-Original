import random

import fx
import pygame
from animations import *
from stgs import *


class mPlatform(pygame.sprite.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.groups = game.colliders, game.sprites, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)
        self.pos = pygame.Vector2((self.rect.x, self.rect.y))
        self.player = self.game.player
        self.pause = False
        self.vertical = False
        self.dir = (1, 0)
        self.vel = 5
        self.color = (255, 255, 255)
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        if self.vertical:
            self.dir = (0, 1)

        self.dir = pygame.Vector2(self.dir).normalize()

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.render()
    
    def render(self):
        defaultTile = Spritesheet(asset('../../CyberSpacePygame/assets/Tiled/tileset1.png')).get_image(0, 0, 32, 32)
        for x in range(0, self.image.get_width(), 32):
            self.image.blit(defaultTile, (x, 0))
    
    def update(self):
        if not self.pause:
            self.move()
            self.rect.x, self.rect.y = self.pos
    
    def move(self):
        testVec = pygame.Vector2((self.pos.x, self.pos.y))
        if self.collideCheck(pygame.Vector2(testVec.x+(self.dir.x*self.vel), testVec.y)):
            
            if self.dir.x > 0:
                self.dir = self.dir.reflect((-1,0))
            else:
                self.dir = self.dir.reflect((1,0))
        
        self.pos.x += self.dir.x*self.vel
        # If we hit player move the player
        testRect = pygame.Rect(self.pos.x, self.pos.y, self.rect.width, self.rect.height)
        if testRect.colliderect(self.player.rect):
            if self.dir.x < 0:
                self.player.rect.right = testRect.left
            else:
                self.player.rect.left = testRect.right

        if self.collideCheck(pygame.Vector2(testVec.x, testVec.y+(self.dir.y*self.vel))):
            if self.dir.y > 0:
                self.dir = self.dir.reflect((0, -1))
            else:
                self.dir = self.dir.reflect((0, 1))
        
        if self.dir.y > 0:
            moveP = self.checkPlayerAbove(testRect)
        else:
            moveP = False

        self.pos.y += self.dir.y*self.vel
        testRect = pygame.Rect(self.pos.x, self.pos.y, self.rect.width, self.rect.height)
        if moveP:
            self.player.rect.bottom = testRect.top
        
        testRect = pygame.Rect(self.pos.x, self.pos.y, self.rect.width, self.rect.height)
        if testRect.colliderect(self.player.rect):
            if self.dir.y < 0:
                self.player.rect.bottom = testRect.top
            else:
                self.player.rect.top = testRect.bottom

    def collideCheck(self, vector):
            returnVal = False
        
            testRect = pygame.Rect(round(vector.x), round(vector.y), self.rect.width, self.rect.height)
            for obj in self.game.colliders:
                if not obj == self:
                    if testRect.colliderect(obj.rect):
                        returnVal = True

            for obj in self.game.level.sprites:
                if isinstance(obj, platWall):
                    if testRect.colliderect(obj.rect):
                        returnVal = True
                    
            return returnVal

    def checkPlayerAbove(self, testRect):
        upRect = testRect.move(0, -1)
        if upRect.colliderect(self.player.rect):
            return True
        else:
            return False
