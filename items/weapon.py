from .item import Item
from time import time

class Weapon(Item):
    def __init__(self, owner, **kwargs):
        super().__init__(owner, **kwargs)
    def action(self, owner):
        if time() - self.lastUse >= self.delay:
            owner.attackState = "attack"
            self.lastUse = time()
    def getAttackDamage(self):
        return (self.inventoryItem.stats["attackDamage"], False)