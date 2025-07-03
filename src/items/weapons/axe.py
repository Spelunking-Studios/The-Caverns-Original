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
        if self.cache_key not in self._cache:
            self._cache[self.cache_key] = pygame.image.load(
                asset("items", "weapon", "axe.png")
            ).convert_alpha()
        self.renderable = self._cache.get(self.cache_key, None)

        super().make_description()

    def _attack(self, user):
        self._route_attack(user)

    def _player_attack(self, player):
        player.attackState = "attack"
