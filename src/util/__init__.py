import pygame

from .camera import Cam
from .display import Display
from .fabrik import fabrik


class Sprite(pygame.sprite.Sprite):
    
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self, ctx, transform=None):
        if transform:
            ctx.blit(self.image, transform(self.rect))
        else:
            ctx.blit(self.image, self.rect)

    def collide(self, other, type ="circle", type2 = None):

        other = other.get_colliders(type)
        other = other if isinstance(other, list) else [other]
        colliders = self.get_colliders(type)
        colliders = colliders if isinstance(other, list) else [other]
        for o in other:
            for c in colliders:
                if type == "circle":
                    if o.collidecircle(c):
                        return True

                elif type == "rect":
                    if o.colliderect(c):
                        return True
        
        return False

            
    
    def get_colliders(self, type="circle"):
        if type == "mask":
            print("mask")
        elif type == "circle":
            if hasattr(self, "pos"):
                pos = self.pos
            else:
                pos = self.rect.center                

            return [pygame.Circle(pos)]
        else:
            print("I don't know this collide type")
