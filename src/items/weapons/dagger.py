from ..weapon import Weapon
from stgs import asset
import pygame


class Dagger(Weapon):
    """Represents the base dagger"""
    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['attack'] = {
            "cooldown": 0.25,
            "damage": 3,
            "critVariance": 2
        }
        self.stats['categories'] = self.base_categories + ["dagger"]
        self.stats['description'] = "Base dagger"
        if self.cache_key not in self._cache:
            self._cache[self.cache_key] = pygame.image.load(
                asset("items", "weapon", "dagger.png")
            ).convert_alpha()
        self.renderable = self._cache.get(self.cache_key, None)

    def _attack(self, user):
        self._route_attack(user)
        print("Dagger action")

    def _player_attack(self, player):
        player.attackState = "attack"
