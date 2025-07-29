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
            "_weight": 10
        }
        self.stats['categories'] = self.base_categories + ["dagger"]
        self.stats['description'] = "Base dagger"
        if self.cache_key not in self._cache:
            self._cache[self.cache_key] = pygame.image.load(
                asset("items", "weapon", "dagger.png")
            ).convert_alpha()
        self.renderable = self._cache.get(self.cache_key, None)

        super().make_description()

    def _player_attack(self, player):
        player.attackState = "attack"
