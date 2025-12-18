import pygame
from src.stgs import *
from .item import Item

class Shield(Item):
    kind = "Shield"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['properties'] = {
            "defense": 2,
            "_weight": 25
        }
        self.stats["buffs"] = {
            "speed": -30
        }
        self.stats['categories'] = self.base_categories + ["shield"]
        self.stats['description'] = "A sturdy shield"
        if self.cache_key not in self._cache:
            self._cache[self.cache_key] = pygame.image.load(
                asset("items", "weapon", "shield.png")
            ).convert_alpha()
        self.renderable = self._cache.get(self.cache_key, None)


    def action(self, user):
        super().action(user)
        user.shield.activate()
        self.stats["buffs_active"] = True

    def unaction(self, user):
        user.shield.deactivate()
        self.stats["buffs_active"] = False
