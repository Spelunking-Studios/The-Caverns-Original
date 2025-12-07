import pygame
from src.stgs import *
from src.items import Item

class Gloves(Item):
    kind = "Gloves"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['categories'] = self.base_categories + ["wearable", "gloves"]
        self.stats['description'] = "A mysterious pair of gloves"

class GlovesStrength(Gloves):
    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['description'] = "A hefty pair of old leather gloves. You feel stronger wearing them."
        self.set_image(
            asset("items", "equipment", "gloves_of_strength.png")
        )
        self.renderable = self._cache.get(self.cache_key, None)

