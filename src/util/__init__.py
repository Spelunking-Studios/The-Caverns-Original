import pygame, pymunk

from .camera import Cam
from .display import Display
from .fabrik import fabrik
from .grouper import Grouper
from .handler import Handler


class Sprite(pygame.sprite.Sprite):
    """Basic sprite class

    Aims to create an interface between the game framework
    and pygame sprites. Attempts to provide compatibility 
    for multiple movement and draw options
    
    All functions aside from __init__ are optional for 
    function
    """
    def __init__(self, *args):
        super().__init__(*args)

    def create_physics(self, mass, radius, vel_func = None, pos = (0, 0)):
        # Set up a body
        self.body = pymunk.Body(mass, 2)# body_type=pymunk.Body.KINEMATIC), 2
        self.body.position = pos
        self.body.friction = 99
        self.body.owner = self
        
        # Attach a circular shape to the body
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.elasticity = 0
        self.shape.friction = 1
        self.shape.sensor = False

        self.game.space.add(self.body, self.shape)
        if vel_func:
            self.body.velocity_func = vel_func

    def set_position(self, pos, centered = False):
        if hasattr(self, "body"):
            self.body.position = pos
            if centered:
                self.rect.center = pos
            else:
                self.rect.topleft = pos

            
        elif hasattr(self, "pos"):
            self.pos = pygame.Vector2(pos)
        else:
            if centered:
                self.rect.center = pos
            else:
                self.rect.topleft = pos

    def draw(self, ctx, transform=None):
        if transform:
            ctx.blit(self.image, transform(self.rect))
        else:
            ctx.blit(self.image, self.rect)

    
    def kill(self):
        super().kill()
        if hasattr(self, "body"):
            self.game.space.remove(self.body, *self.body.shapes)
