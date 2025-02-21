import pygame
import util

gs = util.Sprite()


group = pygame.sprite.Group()
group.add(gs)

gt = util.Sprite(group)

for s in group:
    print(s)

print("Success!")
