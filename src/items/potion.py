from .item import Item
import pygame
from stgs import asset


class DangerousPotion(Item):
    """Critical"""

    kind = "Potion"

    def __init__(self):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats["categories"] = self.base_categories + ["sword"]
        self.stats["description"] = "
        if self.cache_key not in self._cache:
            self._cache[self.cache_key] = pygame.image.load(
                    asset("items", "weapon", "sword.png")
                ).convert_alpha()
        self.renderable = self._cache.get(self.cache_key, None)
        
    def _attack(self, user):
        self._route_attack(user)
        print("Sword action")

    def _player_attack(self, player):
        player.attackState = "attack"
