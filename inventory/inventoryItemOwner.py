class InventoryItemOwner:
    """Represents an owner of an InventoryItem"""
    def __init__(self, item, name, **kwargs):
        """
        Initializes the InventoryItemOwner object.

        Arguments:
        -----
        item: InventoryItem
            The inventory item this owner is owning
        name: string
            The name of the owner
        """
        self.item = item
        self.name = name
        self.obtained = None
        for key, value in kwargs.items():
            self.__dict__[key] = value