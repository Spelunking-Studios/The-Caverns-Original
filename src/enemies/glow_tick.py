import pygame
import random
from src.enemies.enemy import SimpleEnemy
from src.animations import Animator, HurtFx
from src.util import LightSource
from src.stgs import *

class GlowTick(SimpleEnemy):

    def __init__(self, game, pos, **kwargs):
        self.speed = 4
        self.erraticness = 5 # The greater the value, the less erratic

        super().__init__(game, None, **kwargs)

        self.animations = Animator({
            "default": asset("enemies/glow tick/glow_tick.png")
        })
        
        self.rect = pygame.Rect(0, 0, 4, 4)
        self.rect.center = pos
        self.vel = pygame.Vector2(self.speed, 0)
        self.light = LightSource(game, self.rect.copy(), power="0.6", radius=20)
        print(self.rect)

    def update(self):
        super().update()
        self.move(1)
        self.light.position = self.rect.center

    def move(self, dt):
        self.rect.x += self.vel.x*dt
        self.rect.y += self.vel.y*dt
        for zone in self.game.groups.zones:
            if self.rect.colliderect(zone.rect):
                #Consider changing direction
                if random.randint(1, self.erraticness) == 1:
                    if self.vel.x == 0:
                        # Decide to go left or right in new direction
                        self.vel.x = self.speed*random.randrange(-1,2,2)
                        self.vel.y = 0
                    else:
                        self.vel.y = self.speed*random.randrange(-1,2,2)
                        self.vel.x = 0
                return
        
        # Bug was not in a zone, needs to turn around
        self.vel *= random.randrange(-1,2,2)



    def draw(self, ctx, transform=None):
        self.image = self.animations.get_image()
        return super().draw(ctx, transform)
