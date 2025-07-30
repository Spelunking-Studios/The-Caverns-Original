import pygame, pymunk
from pygame import Vector2 as Vec
from src.stgs import *
from src import util

class Shield(util.Sprite):
    image = asset("player/shield.png")
    def __init__(self, game, **kwargs):
        self.game = game
        self.groups = game.sprites, game.layer1
        super().__init__(self.groups)

        self.active = False
        self.distance_from_player = 30 # from center of player
        self.src_image = pygame.image.load(self.image)
        self.image = self.src_image.copy()
        
        self.dump(kwargs) 
        
        self.create_physics() 
    
    def create_physics(self):
        self.body = pymunk.Body(100, 2)
        w, h = self.image.get_size()
        self.shape = pymunk.Poly.create_box(self.body, (w, h))
        self.shape.collision_type = 1
        self.shape.friction = 0.5
        self.rect = pygame.Rect(0, 0, w, h)

    def update(self):
        player = self.game.player

        offset = Vec(0, -self.distance_from_player).rotate(-1*player.angle)
        self.body.position = player.body.position + offset
        self.rect.center = self.body.position
        self.rotate(round(player.angle, 1))

    def rotate(self, angle = 0):
        self.image = pygame.transform.rotate(self.src_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, ctx, transform=None):
        if self.active:
            print(now())
            super().draw(ctx, transform)
