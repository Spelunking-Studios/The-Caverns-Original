import pygame
from pygame.sprite import Group

class Grouper:
    '''A class to control and manipulate multiple groups (pygame.group.Group)
    of game objects that is mainly designed for in code control'''

    def __init__(self):
        """Contains helpful groups for organizing different types of sprites"""


        #### Create sprite groups here ####

        self.players = Group()
        self.enemies = Group()
        self.lightSources = Group()
        self.colliders = Group()
        self.interactable = Group()  # Sprites that can be interacted with
        self.pProjectiles = Group()  # Player Projectiles
        self.eProjectiles = Group()  # Enemy Projectiles
        self.particle_emitters = Group()
        self.zones = Group() # Zones where enemies can spawn

    def getProximitySprites(self, sprite, proximity=300, groups=[]):
        """Returns a list of sprites that fall within the specified proximity\
        to the specified sprite.

        Arguments:
        ----------
        sprite: The sprite that the proximity will be around
        proximity (default=300): The max distance from the sprite another\
        sprite can be
        groups (default=[]): The groups in which entities can be
        found
        """
        groups = groups if isinstance(groups, list) else [groups]
        returnList = []

        for group in groups:
            for ent in group:
                ent_center = pygame.Vector2(ent.rect.center)
                sprite_center = pygame.Vector2(sprite.rect.center)
                dist = ent_center.distance_to(sprite_center)
                if dist <= proximity:
                    returnList.append(ent)

        return returnList

    def clearAll(self):
        for g in self.allGroups():
            g.empty()

    def killAll(self):
        for g in self.allGroups():
            for s in g:
                s.kill()

    def allGroups(self):
        return [self.__dict__[g] for g in self.__dict__ if isinstance(self.__dict__[g], Group)]


