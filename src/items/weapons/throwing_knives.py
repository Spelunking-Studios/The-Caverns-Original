import pygame
from src.stgs import *
from src.items import Weapon


class ThrowingKnives(Weapon):
    '''Pretty self explanatory'''

    kind = "projectile"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['attack'] = {
            "cooldown": 0.3,
            "damage": 7,
            "_variance": 1,
            "_ranged": True,
            "_range": True,
        }
        self.stats['categories'] = self.base_categories + ["throwing_knives"]
        self.stats['description'] = "A dangerous set of knives waiting to be tossed"
        if self.cache_key not in self._cache:
            self._cache[self.cache_key] = pygame.image.load(
                asset("items", "weapon", "throwing_knives.png")
            ).convert_alpha()
        self.renderable = self._cache.get(self.cache_key, None)
        super().make_description()

    def _attack(self, user):
        self._route_attack(user)

    def _player_attack(self, player):
        # player.attackState = "attack"

        # Launches fireball
        player.game.get_prefab("ThrowingKnife")(player.game)
