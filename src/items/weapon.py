from .item import Item
from random import randint


class Weapon(Item):
    base_categories = ["weapon"]
    kind = "Generic Weapon"

    def __init__(self):
        super().__init__()
        self.stats["categories"] = ["weapon"]
        self.stats["attack"] = {
            "damage": 1,
            "cooldown": 1
        }

    def bruh_ben(self):
        # Gives item statistics easy access :)
        for k, v in self.stats["attack"].items():
            self.__dict__[k] = v

    def _route_attack(self, user):
        if (
            user.__class__.__name__ == "Player" and
            hasattr(self, "_player_attack")
        ):
            self._player_attack(user)
        else:
            self._base_attack()

    def _base_attack(self, user):
        print("\x1b[93\
        WARNING: Base attack for " + self.__class__.__name__ + " \
        was used by " + user.__class__.__name__ + ", \
        but it doesn't do anything.\
        \x1b[0m")

    def _attack(self, user):
        self._route_attack()

    def get_attack_damage(self, user):
        return self.stats["attack"]["damage"], randint(0, 5) == 0
