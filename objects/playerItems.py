import pygame
from .projectiles import Fireball

class Sword1:
    '''Default sword'''
    def __init__(self):
        self.lastAttack = 0
        self.attackDelay = 20
        self.damage = 7
        self.atkVariance = 1

    def action(self, player):
        '''Allows item to function via the player'''
        self.player = player
        now = pygame.time.get_ticks()
        if now - self.lastAttack >= self.player.stats.atkSpeed+self.attackDelay:
            self.player.animations.setMode('hit')
            self.lastAttack = now

class MagicWand:
    '''A magic wielding wand'''
    def __init__(self):
        self.lastAttack = 0
        self.attackDelay = 30
        self.damage = 12
        self.atkVariance = 0
    
    def action(self, player):
        '''Allows item to function via the player'''
        self.player = player
        now = pygame.time.get_ticks()
        if now - self.lastAttack >= self.player.stats.atkSpeed+self.attackDelay:
            self.player.animations.setMode('wand')
            Fireball(self.player.game)
            self.lastAttack = now