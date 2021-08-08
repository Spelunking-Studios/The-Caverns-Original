import random

import fx
import pygame
from animations import *
from stgs import *

class coinMeter(pygame.sprite.Sprite):

    def __init__(self, game, player, **kwargs):
        self.groups = game.sprites, game.overlayer
        pygame.sprite.Sprite.__init__(self, self.groups)

        ## Setup
        self.x = 0
        self.y = 40
        self.width = 30
        self.height = 100
        self.bgColor = colors.rgba(colors.light(colors.black, 20), 120)
        self.coinColor = colors.yellow
        self.offset = 5
        self.gap = self.offset*2
        
        self.meterLevel = 0
        self.coins = 0
        self.coinsPerLevel = 5
        self.healthAddPerc = 0.2
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.player = player
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.barRect = pygame.Rect(self.offset, self.offset, self.width-self.gap, self.height-self.gap)
        
    
    def update(self):
        self.image.fill((self.bgColor))
        self.renderBar()
    
    def renderBar(self):
        pygame.draw.rect(self.image, self.coinColor, (self.barRect.x, self.barRect.y+(self.barRect.height)*(1 - self.meterLevel/self.coinsPerLevel), self.barRect.width, (self.barRect.height)*(self.meterLevel/self.coinsPerLevel)))

    def addCoin(self):
        self.coins += 1
        self.meterLevel += 1
        if self.meterLevel >= self.coinsPerLevel:
            self.meterLevel = 0
            self.player.health += self.player.maxHp*self.healthAddPerc
            self.player.health = min(self.player.maxHp, self.player.health)
