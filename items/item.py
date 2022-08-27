from inventory import InventoryItem

class Item:
    """Represents a basic item"""
    def __init__(self, owner, **kwargs):
        """
        Initializes the item

        Arguments:
        -----
        owner
            The owner of the item.
            Note: the owner must have an inventory property that is a Inventory object
        surpressIICreation: boolean = False
            Prevent the item from creating an InventoryItem object.
            Only use this when you will be setting the object or don't want the
            item to be visible in the inventory menu.
        """
        self.owner = owner
        self.surpressIICreation = False
        hasImage = False
        for key, value in kwargs.items():
            self.__dict__[key] = value
        if not self.surpressIICreation:
            self.inventoryItem = InventoryItem(self.owner.inventory, "Item")