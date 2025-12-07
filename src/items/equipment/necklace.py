import pygame
from src.stgs import *
from src.items import Item

class Necklace(Item):
    kind = "Necklace"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['categories'] = self.base_categories + ["wearable", "necklace"]
        self.stats['description'] = "A mysterious Necklace"
        self.stats["buffs"] = {
            "healthMax": 10000
        }

class NecklaceAlerting(Necklace):
    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['description'] = "An old bronze Necklace with an engraving of a bat on it"
        self.set_image(
            asset("items", "equipment", "necklace_of_alerting.png")
        )

    def equip(self, game):
        game.alert_hud.activate()
        super().equip()

    def unequip(self, game):
        game.alert_hud.deactivate()
        super().unequip()
