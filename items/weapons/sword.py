from ..weapon import Weapon
from inventory import InventoryItem
from time import time

class Sword(Weapon):
    """Represents the base sword"""
    def __init__(self, owner):
        super().__init__(owner, surpressIICreation = True)
        self.damage = 1
        self.delay = 0.5
        self.lastUse = -1
        hasImage = True
        self.inventoryItem = InventoryItem(
            self.owner.inventory,
            "Sword",
            groups = ["Weapon", "Sword"],
            category = "Weapon",
            description = "Base Sword",
            owners = [self],
            stats = {
                "attackDamage": 5
            }
        )
