from ..weapon import Weapon
import pygame
from src.stgs import asset


class Axe(Weapon):
    kind = "Axe"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['attack'] = {
            "cooldown": 0.8,
            "damage": 20,
            "_variance": 1,
            "_weight": 25
        }
        self.stats['categories'] = self.base_categories + ["axe"]
        self.stats['description'] = "Axe"
        self.set_image(
            asset("items", "weapon", "axe.png")
        )

        super().make_description()

    def _player_attack(self, player):
        player.attackState = "attack"
