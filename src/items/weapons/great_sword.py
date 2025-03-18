from ..weapon import Weapon
import pygame
from stgs import asset


class GreatSword(Weapon):
    """Represents the base sword"""

    kind = "Great Sword"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats["attack"] = {
            "cooldown": 3,
            "damage": 21,
            "critVariance": 7
        }
        self.stats["categories"] = self.base_categories + ["sword"]
        self.stats["description"] = "Great sword"
        if self.cache_key not in self._cache:
            self._cache[self.cache_key] = pygame.image.load(
                asset("items", "weapon", "sword.png")
            ).convert_alpha()
        self.renderable = self._cache.get(self.cache_key, None)

    def _attack(self, user):
        self._route_attack(user)
        print("Great Sword action")

    def _player_attack(self, player):
        player.attackState = "attack"
