import random
import util
import fx
import pygame, pymunk
import pymunk.autogeometry
from pygame import Vector2 as Vec
from animations import *
from stgs import *

def is_clockwise(points):
    """Return True if the polygon is wound clockwise."""
    area = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        area += (x2 - x1) * (y2 + y1)
    return area > 0

class Wall(util.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.groups.colliders, game.layer1 if DEBUG else game.groups.colliders
        super().__init__(self.groups)
        self.objT = objT
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        if "points" in objT.__dict__:
            # If the shape is a polygon we take the points and fix them
            points = []
            for p in objT.points:
                points.append(tuple(p))
            if points[0] != points[-1]:
                points.append(points[0])
            if is_clockwise(points):
                points.reverse()
            # Decomposes complex polygons to pymunk friendly ones
            parts = pymunk.autogeometry.convex_decomposition(points, 0.2)
            for part in parts:
                self.shape = pymunk.Poly(game.space.static_body, part)
                self.shape.friction = 0.5
                self.game.space.add(self.shape)
        else:
            self.body.position = self.rect.center
            self.shape = pymunk.Poly.create_box(self.body, (objT.width, objT.height))

            self.shape.friction = 0.5
            self.game.space.add(self.body, self.shape)

        self.color = (255, 255, 255)
        self.targetObj = "Entrance"
        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        if DEBUG:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(self.color)

    def draw(self, ctx, transform):
        if DEBUG_PHYSICS:
             pygame.draw.rect(ctx, colors.white, transform(self.rect))
