import pygame
import random
import src.util

# def get_random_zone_position(game):
#
#     def in_zone(point):
#         p = pygame.Rect(*point, 1, 1)
#         for z in game.groups.zones:
#             if z.rect.colliderect(p):
#                 return True
#         return False
#
#     level_w, level_h = game.map.floor.room.rect.size
#     point = (random.random()*level_w, random.random()*level_h)
#     out = in_zone(point)
#     while not out:
#         level_w, level_h = game.map.floor.room.rect.size
#         point = (random.random()*level_w, random.random()*level_h)
#         out = in_zone(point)
    # return point

# def get_random_zone_position(game):
    # level_w, level_h = game.map.floor.room.rect.size
    # point = (random.random()*level_w, random.random()*level_h)
    # return point
    #
def get_random_zone_position(game):
    weights = []
    for z in game.groups.zones.sprites():
        area = z.rect.w*z.rect.h
        weights.append(area)
    zone = random.choices(game.groups.zones.sprites(), weights=weights, k=1)[0]
    return zone.random_position()
