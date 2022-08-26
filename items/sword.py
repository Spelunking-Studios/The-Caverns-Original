from .item import Item
from inventory import InventoryItem
from time import time

class Sword(Item):
    """Represents the base sword"""
    def __init__(self, owner):
        super().__init__(owner, surpressIICreation = True)
        self.damage = 1
        self.delay = 0.5
        self.lastUse = -1
        self.inventoryItem = InventoryItem(
            self.owner.inventory,
            "Sword",
            groups = ["Weapon", "Sword"],
            category = "Weapon",
            description = "Base Sword",
            owners = [self]
        )
    def action(self, owner):
        if time() - self.lastUse >= self.delay:
            owner.animations.setMode('hit')
            self.lastUse = time()
