import json
import src.items
from src.items import Item

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

    # I don't foresee slowdowns by calculating the player's buffs
    # but in case there are here is the outline of a caching 
    # method to prevent this
    #
    # @staticmethod
    # def cache(func):
    #      cache_list
    #     def cached_func(*args):
    #           if args in cache_list:
    #               return cache_list[args]
    #           else:
    #               cache_list[args].append(blah blaj)
    #               func()
    #
    # @cache

    def get_buffs(self, query):
        sum = 0
        for i in self.get_items():
            item = self.get_item(i)
            if item.stats["buffs_active"] and query in item.stats["buffs"]:
                sum += item.stats["buffs"][query]

        return sum

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
        allowed_items = [src.items.__dict__[i] for i in src.items.__all__]

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
