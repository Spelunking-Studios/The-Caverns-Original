import random

import fx
import pygame
from animations import *
from stgs import *


class healthBar(pygame.sprite.Sprite):
    x = winWidth/3
    y = 3
    width = 100
    height = 30
    bgColor = colors.light(colors.black, 50)
    hpColor = colors.lightGreen
    offset = 10
    gap = offset
    def __init__(self, game, player, **kwargs):
        self.groups = game.sprites, game.overlayer
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.player = player
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.barRect = pygame.Rect(self.offset/2, self.offset/2, self.width-self.gap, self.height-self.gap)
    
    def update(self):
        self.image.fill((self.bgColor))
        self.renderBar()
    
    def renderBar(self):
        pygame.draw.rect(self.image, self.hpColor, (self.barRect.x, self.barRect.y, (self.barRect.width)*(self.player.health/self.player.maxHp), self.barRect.height))
    # def renderBar(self):
    #     pygame.draw.rect(self.image, self.hpColor, (1, 1, (self.barRect.width)*(self.player.health/self.player.maxHp), self.barRect.height))

class healthBar2(healthBar):
    x = 5
    y = winHeight/3
    width = 30
    height = 100
    bgColor = colors.light(colors.black, 100)
    offset = 6
    gap = offset

    def __init__(self, game, player):
        super().__init__(game, player)
    def renderBar(self):
        pygame.draw.rect(self.image, self.hpColor, (self.barRect.x, self.barRect.y+(self.barRect.height)*(1 - self.player.health/self.player.maxHp), self.barRect.width, (self.barRect.height)*(self.player.health/self.player.maxHp)))
