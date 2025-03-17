import pygame

from .camera import Cam



class Sprite(pygame.sprite.Sprite):
    
    def draw(self, ctx, transform=None):
        if transform:
            ctx.blit(self.image, transform(self.rect))
        else:
            ctx.blit(self.image, self.rect)

