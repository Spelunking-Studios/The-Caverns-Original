from random import randint
from src.stgs import *

class Stats:
    def __init__(self, **kwargs):
        # This will be used to set default values for properties that can be used
        self.health = 0
        self.strength = 0 # This will become a modifier for damage
        self.speed = 0
        self.attack_damage = 0 # This will not be used on the player because it will have a more complicated damage calculator
        self.attack_variance = 1
        self.crit = 5

        for k, v in kwargs.items():
            self.__dict__[k] = v

    def setValues(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def attack(self):
        damage = randint(max(0, self.attack_damage-self.attack_variance), self.attack_damage+self.atkVariance)
        return damage

    def isDead(self):
        return bool(self.health <= 0)


class PlayerStats(Stats):
    def __init__(self, player):
        if DEBUG:
            super().__init__(
                    health=230,
                    healthMax=230,
                    stamina=50,
                    staminaMax=50,
                    strength=10,
                    speed=120,
                    attack_variance=1,
                    attack_speed=400, # This is a delay in milliseconds
                    defense=15,
                    crit=5, # This is a percent out of 100 (make sure its an integer)
                    critBonus = 200, # This is a percent
                    sprint_multiplier = 2
                    )
        else:
            super().__init__(
                    health=30,
                    healthMax=30,
                    stamina=50,
                    staminaMax=50,
                    strength=10,
                    speed=30,
                    attack_variance=1,
                    attack_speed=400, # This is a delay in milliseconds
                    defense=15,
                    crit=5, # This is a percent out of 100 (make sure its an integer)
                    critBonus = 200, # This is a percent
                    sprint_multiplier = 2
                    )
        self.player = player
        self.inventory = player.inventory

    def attack(self, weapon = None): # The index here just means which hotbar number the action is
        if self.player.last_action == 1:
            dmg = self.player.slot1.damage + self.strength/5
        else:
            dmg = self.player.slot2.damage + self.strength/5
        variance = self.player.slot1._variance if self.player.last_action == 1 else self.player.slot2._variance
        atkVar = self.attack_variance + variance
        if randint(0, 100) <= self.crit:
            crit = True
            damage = randint(max(0, int((dmg-atkVar)*(self.critBonus/100))), int((dmg+atkVar)*(self.critBonus/100)))
            print("DAMN YOU HIT A CRITICAL")
        else:
            crit = False
            damage = randint(int(max(0, dmg-atkVar)), int(dmg+atkVar))

        return damage, crit

    # Reset the stats after the player dies and is respawned in
    def reset(self):
        self.health = self.healthMax


class Inventory:
    def __init__(self, *args, **kwargs):
        self.slotMax = 5
        self.slots = {}
        self.slotFocus = 1
        # self.sprite = sprite
        for k, v in kwargs.items():
            self.__dict__[k] = v

        for x in range(1, self.slotMax+1):
            try:
                self.slots[x] = args[x-1]
            except IndexError:
                self.slots[x] = None

    def setSlot(self, index, item=None):
        if not index > self.slotMax:
            self.slots[index] = item
        self.slotFocus = index

    def getSlot(self, index):
        self.slotFocus = index
        if not index > self.slotMax:
            return self.slots[index]

    def getIndex(self, item):
        for k, v in self.slots.items():
            if v == item:
                return k
        return None

    def getCurrent(self):
        return self.slots[self.slotFocus]

    def expand(self, increase, *args):
        for x in range(self.slotMax, self.slotMax+increase):
            try:
                self.slots[x] = args[x-self.slotMax]
            except IndexError:
                self.slots[x] = None
        self.slotMax += increase
