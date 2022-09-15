from .inventoryItemOwner import InventoryItemOwner
import pygame

class InventoryItem:
    """Represents an inventory item"""
    def __init__(self, inventory, name, **kwargs):
        """
        Initializes the InventoryItem

        Arguments:
        -----
        inventory: Inventory
            The inventory object the item belongs to
        name
            The name of the item
        """
        self.inventory = inventory
        self.name = name
        self.owners = []
        self.stats = {}
        self.groups = ["All"]
        self.category = "General"
        #self.image = pygame.Surface((50, 50), pygame.SRCALPHA).convert_alpha()
        self.description = ""
        for key, value in kwargs.items():
            self.__dict__[key] = value