from items import Item


class Inventory:
    def __init__(self):
        self._registry = {
            "items": {}
        }

    def add_item(self, item):
        """Add an item to the inventory"""

        name = item.__class__.__name__
        entry = self._registry["items"].get(name, None)

        # Only add instances of Item
        if isinstance(item, Item):
            # If the item's class has an entry, append the item

            if entry:
                entry["items"].append(item)

            # Otherwise, make an new entry
            else:
                self._registry["items"][name] = {
                    "items": [item]
                }
        else:
            print(
                "\x1b[93mWARNING:",
                "Item of type",
                name,
                "was not added to the inventory",
                "becasue it is not a instance of Item.\x1b[0m"
            )

        # Return either the entry or None
        return self._registry["items"].get(name, None)

    def get_items(self):
        return self._registry["items"]
