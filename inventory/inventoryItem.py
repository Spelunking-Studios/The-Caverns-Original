from .inventoryItemOwner import InventoryItemOwner
import pygame

class InventoryItem:
    """Represents an inventory item"""
    def __init__(self, inventory, **kwargs):
        """
        Initializes the InventoryItem

        Arguments:
        -----
        inventory: Inventory
            The inventory object the item belongs to
        """
        self.inventory = inventory
        self.owners = []
        self.stats = {}
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA).convert_alpha()
        self.description = ""
        for key, value in kwargs.items():
            self.__dict__[key] = value