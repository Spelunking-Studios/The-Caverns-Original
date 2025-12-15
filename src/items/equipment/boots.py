import pygame
from src.stgs import *
from src.items import Item

class Boots(Item):
    kind = "Gloves"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['categories'] = self.base_categories + ["wearable", "boots"]
        self.stats['description'] = "A mysterious pair of Boots"

class BootsSpeed(Boots):
    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['description'] = "A curious pair of army issued boots inscribed with a gold symbol of Lugus"
        self.stats["buffs"] = {
            "speed": 10,
            "staminaMax": 10,
        }
        self.set_image(
            asset("items", "equipment", "gloves_of_strength.png")
        )

