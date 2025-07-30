from src import util
import pygame
import pymunk
import pymunk.autogeometry
from src.animations import *
from src.stgs import *


def is_clockwise(points):
    """Return True if the polygon is wound clockwise."""
    area = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        area += (x2 - x1) * (y2 + y1)
    return area > 0

class Wall(util.Sprite):
    '''
    Wall object. Has a collision type of 1. Relies on the pymunk static_body object. 
    Supports infinite vertices
    '''
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.groups.colliders, game.layer1 if DEBUG else game.groups.colliders
        super().__init__(self.groups)
        self.objT = objT
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        
        self.shapes = []
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
                shape = pymunk.Poly(game.space.static_body, part)
                shape.friction = 0.5
                shape.collision_type = 1
                self.game.space.add(shape)
                self.shapes.append(shape)
            self.game.space.add(self.body)
        else:
            self.body.position = self.rect.center
            self.shape = pymunk.Poly.create_box(self.body, (objT.width, objT.height))
            self.shape.collision_type = 1

            self.shape.friction = 0.5
            self.game.space.add(self.body, self.shape)

        self.color = (255, 255, 255)
        self.targetObj = "Entrance"
        self.dump(kwargs, objT.properties) 

        if DEBUG:
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(self.color)

    def draw(self, ctx, transform):
        if DEBUG_PHYSICS:
             pygame.draw.rect(ctx, util.white, transform(self.rect))

    def kill(self):
        for shape in self.shapes:
            try:
                self.game.space.remove(shape)
            except AssertionError:
                print("Error: wall shape not in space")
        return super().kill()
