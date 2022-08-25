from .inventoryItem import InventoryItem

class Inventory:
    """Represents an inventory"""
    def __init__(self, entity):
        """
        Initializes the inventory

        Arguments:
        -----
        entity: any
            The entity the inventory belongs to
        """
        self.entity = entity