import pygame
from src.stgs import *
from src.items import Weapon


class Wand(Weapon):
    '''A magic wielding wand'''

    kind = "magic"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['attack'] = {
            "cooldown": 0.8,
            "damage": 20,
            "_variance": 1,
            "ranged": True,
        }
        self.stats['categories'] = self.base_categories + ["dagger"]
        self.stats['description'] = "Base dagger"
        if self.cache_key not in self._cache:
            self._cache[self.cache_key] = pygame.image.load(
                asset("items", "weapon", "dagger.png")
            ).convert_alpha()
        self.renderable = self._cache.get(self.cache_key, None)
        print("kyle was here")
        super().make_description()

    def _attack(self, user):
        self._route_attack(user)

    def _player_attack(self, player):
        # player.attackState = "attack"
    
        # player.animations.setMode('wand')
        # Launches fireball
        player.game.get_prefab("Fireball")(player.game)
