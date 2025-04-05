import pygame
from pygame import Vector2 as Vec
from src.stgs import *
from src.util import Sprite

class SimpleChain(Sprite):
    """A sprite responsible for computing the points of a chain
    
    Does not draw to screen
    
    """

    def __init__(self, game, owner, length, dists):
        super().__init__((game.sprites))
        self.game = game
        self.owner = owner
        self.reset = True
        
        self.chain_len = length
        self.chain_distances = dists
        self.chain = [Vec(0, i*self.chain_distances[i-1]) for i in range(self.chain_len)]
        self.chain_angles = [0.0 for i in range(self.chain_len)]
        self.radius = 5 
        self.pos = Vec(20, 20) # Head position
        self.rect = pygame.Rect(*self.pos, self.radius*2, self.radius*2)
        self.image = pygame.Surface(self.rect.size)

    def update(self):
        self.update_chain()

    def get_colliders(self, type):
        if type == "circle":
            return [pygame.geometry.Circle(c, self.radius) for c in self.chain]
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

