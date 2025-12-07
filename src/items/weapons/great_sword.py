from ..weapon import Weapon
import pygame
from src.stgs import asset


class GreatSword(Weapon):
    """Massive fricking sword"""

    kind = "Great Sword"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats["attack"] = {
            "cooldown": 3,
            "damage": 210,
            "_variance": 1,
            "_weight": 920
        }
        self.stats["categories"] = self.base_categories + ["sword"]
        self.stats["description"] = "Great sword"
        self.set_image(
            asset("items", "weapon", "sword.png")
        )

        super().make_description()

    def _player_attack(self, player):
        player.attackState = "attack"
