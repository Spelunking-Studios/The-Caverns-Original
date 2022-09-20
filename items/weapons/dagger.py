from ..weapon import Weapon
from inventory import InventoryItem
from time import time

class Dagger(Weapon):
    """Represents the base dagger"""
    def __init__(self, owner):
        super().__init__(owner, surpressIICreation = True)
        self.damage = 0.2
        self.delay = 0.25
        self.lastUse = -1
        hasImage = True
        self.inventoryItem = InventoryItem(
            self.owner.inventory,
            "Dagger",
            groups = ["Weapon", "Dagger"],
            category = "Weapon",
            description = "Base Dagger",
            owners = [self],
            stats = {
                "attackDamage": 5
            }
        )
