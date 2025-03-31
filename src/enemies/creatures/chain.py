import pygame
from pygame import Vector2 as Vec
from src.stgs import *

class SimpleChain(pygame.sprite.Sprite):
    def __init__(self, game, length, dists):
        super().__init__((game.sprites))
        self.game = game
        self.reset = True
        
        self.chain_len = length
        self.chain_distances = dists
        self.chain = [Vec(0, i*self.chain_distances[i-1]) for i in range(self.chain_len)]
        self.chain_angles = [0.0 for i in range(self.chain_len)]
        
        self.pos = Vec(20, 20) # Head position

    def update(self):
        self.update_chain()


    def update_chain(self):
        self.chain[0] = self.pos
       
        for i in range(1, len(self.chain)):
            delta = self.chain[i] - self.chain[i-1]
            self.chain[i] =  delta.normalize()*self.chain_distances[i-1] + self.chain[i-1]
            self.chain_angles[i] = delta.as_polar()[1]

    def draw(self, surf, transform=None):
        # for i in range(len(self.chain)):
        #     pygame.draw.circle(surf, WHITE, self.chain[i], 5)#self.chain_distances[i]/2)
        pass

