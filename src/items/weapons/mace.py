from ..weapon import Weapon
import pygame
from src.stgs import asset


class Mace(Weapon):
    """Scares of predators with sharp spikes and bludgeoning damage"""

    kind = "Mace"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats["attack"] = {
            "cooldown": 0.4,
            "damage": 8,
            "crit": 0.25,
            "_variance": 4,
            "_weight": 25
        }
        self.stats["categories"] = self.base_categories + ["mace"]
        self.stats["description"] = "A very heavy mace. The spiked head has begun to rust from the blood of countless victims"
        if self.cache_key not in self._cache:
            self._cache[self.cache_key] = pygame.image.load(
                asset("items", "weapon", "mace.png")
            ).convert_alpha()
        self.renderable = self._cache.get(self.cache_key, None)

        super().make_description()

    def _player_attack(self, player):
        player.attackState = "attack"
