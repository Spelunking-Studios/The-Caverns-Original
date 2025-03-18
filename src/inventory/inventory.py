import json
from items import Item, Weapon, Sword, Dagger, GreatSword


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

    def get_item(self, name):
        """Retrives an item from the inventory"""
        return self._registry["items"].get(name, None)

    def get_items(self):
        """Retrives all of the itemes in the inventory"""
        return self._registry["items"]

    def serialize(self):
        """Serialized the inventory into bytes"""
        return json.dumps(
            self._registry,
            default=self._serialize_json_default
        )

    def _serialize_json_default(self, o):
        if isinstance(o, Item):
            stats = o.stats.copy()
            stats.pop("use", None)
            return stats

    def deserialize(self, s):
        """Loads the serialized string into the current object"""
        allowed_items = [Item, Weapon, Sword, GreatSword, Dagger]

        data = json.loads(s)

        for item_name in data["items"]:
            if item_name not in [c.__name__ for c in allowed_items]:
                print(
                    "\x1b[93mWarning:",
                    "item of type",
                    "'" + item_name + "'",
                    "is not a valid item.\x1b[0m"
                )
                continue

            item = data["items"][item_name]
            for item_instance in item["items"]:
                # Recreate the item
                _class = list(filter(lambda c: c.__name__ == item_name, allowed_items))[0]
                new_item = _class()
                new_item.deserialize(item_instance)
                self.add_item(new_item)
