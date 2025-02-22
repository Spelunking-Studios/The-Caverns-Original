from time import time


class Item:
    _cache = {}
    base_categories = []

    def __init__(self):
        self.stats = {
            "categories": [],
            "description": "Base item",
            "use": {
                "fn": self.action,
                "last": -1
            }
        }
        self.renderable = None

    def action(self, user):
        now = time()
        if (
            "attack" in self.stats and
            self.stats["attack"].get("cooldown", 0)
            <
            now - self.stats["use"].get("last", -1)
        ):
            self._attack(user)
            self.stats["use"]["last"] = now

    def deserialize(self, o):
        self.stats = o
        self.stats["use"] = {
            "fn": self.action,
            "last": -1
        }

    def _attack(self, user):
        print("\x1b[93\
        WARNING: Base item was used, but it doesn't do anything.\
        \x1b[0m")
