from .item import Item
from random import randint


class Wearable(Item):
    base_categories = ["wearable"]
    kind = "Generic Weapon"

    def __init__(self):
        super().__init__()
        self.stats["categories"] = ["wearable"]
        self.stats["equipped"] = False
        self.stats["attack"] = {
            "damage": 1,
            "cooldown": 1
        }

    def equip(self, *args):
        self.stats["equipped"] = True
        self.stats["buffs_active"] = True

    def unequip(self):
        self.stats["equipped"] = False
        self.stats["buffs_active"] = False

    # def deserialize(self, o):
    #     super().deserialize(o)
    #     if self.stats["equipped"]:
    #         # Run equip hooks if any
    #         self.equip()
