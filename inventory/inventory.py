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
        self.items = {}
    def addItem(self, item):
        """Adds an item to the inventory
        
        Arguments:
        -----
        item: InventoryItem
            The item to be added to the inventory.
        """
        try:
            self.items[item.name]["items"].append(item)
        except KeyError:
            self.items[item.name] = {
                "description": item.description,
                "category": item.category,
                "items": [item]
            }
    def getItemByName(self, name):
        """Get an item listing for a given name
        
        Arguments:
        -----
        name
            The name of the item

        Returns:
        -----
        The item listing (dict) on a success and False on failure
        """
        try:
            return self.items[name]
        except KeyError:
            return False
    def filter(self, _for, by = "groups"):
        """
        Filter all items by either their groups or cetegory

        Arguments:
        -----
        _for: string
            The string to search the items against
        by: string = "groups"
            The method by which items will be filtered. Must be either "groups" or "category"
        
        Returns:
        -----
        A list of item listings (dict) on a success and and empty list on failure
        """
        return filter(
            lambda item: item != None,
            [item if item[by] == _for else None for item in self.items]
        )