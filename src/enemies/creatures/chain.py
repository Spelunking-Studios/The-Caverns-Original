import pygame
from pygame import Vector2 as Vec
from src.stgs import *
from src.util import Sprite

class SimpleChain(Sprite):
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

    def get_colliders(self, type):
        if type == "circle":
            return [pygame.Circle(c, 5) for c in self.chain]
        else:
            super().get_colliders()


    def update_chain(self):
        self.chain[0] = self.pos
       
        for i in range(1, len(self.chain)):
            delta = self.chain[i] - self.chain[i-1]
            self.chain[i] =  delta.normalize()*self.chain_distances[i-1] + self.chain[i-1]
            self.chain_angles[i] = delta.as_polar()[1]

    def draw(self, surf, transform=None):
        pass

