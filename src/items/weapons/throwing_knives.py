import pygame
from src.stgs import *
from src.items import Weapon


class ThrowingKnives(Weapon):
    '''Pretty self explanatory'''

    kind = "Throwing Knives"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['attack'] = {
            "cooldown": 0.3,
            "damage": 4,
            "_variance": 1,
            "_ranged": True,
            "_range": True,
        }
        self.stats['categories'] = self.base_categories + ["throwing_knives"]
        self.stats['description'] = "A dangerous set of knives waiting to be tossed"
        self.set_image(
            asset("items", "weapon", "throwing_knives.png")
        )
        self.renderable = self._cache.get(self.cache_key, None)
        super().make_description()

    def _player_attack(self, player):
        # player.attackState = "attack"

        # Launches fireball
        player.game.get_prefab("ThrowingKnife")(player.game)
