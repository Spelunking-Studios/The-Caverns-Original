import pygame
import random
from pygame import Vector2 as Vec
from src.stgs import *
from src import util
from src import objects

class PhantomTrail(util.Sprite):
    def __init__(self, game, **kwargs):
        self.game = game

        super().__init__((game.layer2))


        self.last_ghost = 0
        self.frequency = 80 # Delay in milliseconds
        self.color = (255, 0, 0)
        self.length = 20
        self.fade = 8

        self.dump(kwargs)

        self.ghosts = []
        
    def update(self, image, rect):
        if now() - self.last_ghost > self.frequency:
            img = image.copy()
            img.fill(self.color, special_flags = pygame.BLEND_MULT)
            self.ghosts.append((img, rect))
            if len(self.ghosts) > self.length:
                del self.ghosts[0]
            self.last_ghost = now()

        for g in self.ghosts:
            g[0].set_alpha(g[0].get_alpha()-self.fade)


    def draw(self, ctx, transform=None):
        for g in self.ghosts:
            ctx.blit(g[0], transform(g[1]))
            


