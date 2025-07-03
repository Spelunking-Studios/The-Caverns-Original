import json
from src.items import Item, Weapon, Sword, Dagger, GreatSword, Axe, Mace, ThrowingKnives


class Inventory:
    def __init__(self):
        self._registry = {
            "items": {}
        }

    def add_item(self, item):
        """Add an item to the inventory"""

        # Only add instances of Item
        if isinstance(item, Item):
            self._registry["items"][item.id] = item
        else:
            print(
                "\x1b[93mWARNING:",
                "Item of type",
                item.__class__.__name__,
                "was not added to the inventory",
                "becasue it is not a instance of Item.\x1b[0m"
            )

        # Return either the entry or None
        return self._registry["items"].get(item.id, None)

    def get_item(self, item_id):
        """Retrives an item from the inventory"""
        return self._registry["items"].get(item_id, None)

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
            stats["id"] = o.id
            stats["class"] = o.__class__.__name__
            return stats

    def deserialize(self, s):
        """Loads the serialized string into the current object"""
        allowed_items = [Item, Weapon, Sword, GreatSword, Dagger, Axe, Mace, ThrowingKnives]

        data = json.loads(s)

        for item_id in data["items"]:
            item_class = data["items"][item_id]["class"]
            if item_class not in [c.__name__ for c in allowed_items]:
                print(
                    "\x1b[93mWarning:",
                    "item of type",
                    "'" + item_class + "'",
                    "is not a valid item.\x1b[0m"
                )
                continue

            item = data["items"][item_id]
            _class = list(filter(lambda c: c.__name__ == item_class, allowed_items))[0]
            new_item = _class()
            new_item.deserialize(item)
            self.add_item(new_item)
