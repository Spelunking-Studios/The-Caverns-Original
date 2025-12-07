from ..weapon import Weapon
import pygame
from src.stgs import asset


class Sword(Weapon):
    """Represents the base sword"""

    kind = "Sword"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats["attack"] = {
            "cooldown": 0.3,
            "damage": 9,
            "_variance": 2,
            "_weight": 10 
        }
        self.stats["categories"] = self.base_categories + ["sword"]
        self.stats["description"] = "The sword given to you by your father on your 13th birthday. Your name is engraved upon it"
        self.set_image(
            asset("items", "weapon", "sword.png")
        )
        self.renderable = self._cache.get(self.cache_key, None)

        super().make_description()
    
    def _player_attack(self, player):
        player.attackState = "attack"
