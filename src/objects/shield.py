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
        self.src_image = pygame.image.load(self.image)
        self.image = self.src_image.copy()

        self.distance_from_player = 30 # from center of player
        self.padding = 10 # adds a little thickness to the shield
        self.speed_penalty = 0.5
        self.item = None

        
        self.dump(kwargs) 
        
        self.create_physics() 
    
    def create_physics(self):
        self.body = pymunk.Body(10000000, 200000000000, body_type=pymunk.Body.KINEMATIC)
        w, h = self.image.get_size()
        self.shape = pymunk.Poly.create_box(self.body, (w, h+self.padding))
        self.shape.collision_type = 6
        self.shape.friction = 0.5
        self.shape.filter = pymunk.ShapeFilter(group=util.collisions.PLAYER_GROUP)
        self.rect = pygame.Rect(0, 0, w, h)

    def update(self):
        player = self.game.player
        self.item = player.slot2

        if self.active:
            offset = Vec(0, -self.distance_from_player).rotate(-1*player.angle)
            self.body.position = player.body.position + offset
            self.body.angle = player.angle*-0.0175
            self.rect.center = self.body.position
            self.rotate(round(player.angle, 1))

    def activate(self):
        if not self.active:
            self.game.space.add(self.body, self.shape)
            self.active = True

    def deactivate(self):
        if self.active:
            self.game.space.remove(self.body, self.shape)
            self.active = False

    def rotate(self, angle = 0):
        self.image = pygame.transform.rotate(self.src_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, ctx, transform=None):
        if self.active:
            super().draw(ctx, transform)

    def kill(self):
        # Adds body to space for removal
        self.activate()
        super().kill()
