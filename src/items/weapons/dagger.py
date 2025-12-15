from ..weapon import Weapon
from src.stgs import asset
import pygame


class Dagger(Weapon):
    """Represents the base dagger"""

    kind = "Dagger"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['attack'] = {
            "cooldown": 0.2,
            "damage": 3,
            "_variance": 1,
            "_weight": 10,
            "_drain": 4
        }
        self.stats['categories'] = self.base_categories + ["dagger"]
        self.stats['description'] = "Base dagger"
        self.set_image(
            asset("items", "weapon", "dagger.png")
        )
        super().make_description()

    def _player_attack(self, player):
        player.attackState = "attack"
