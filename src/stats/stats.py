from random import randint
from src.stgs import *

class Stats:
    def __init__(self, **kwargs):
        # This will be used to set default values for properties that can be used
        # self.health = 0
        # self.strength = 0 # This will become a modifier for damage
        # self.speed = 0
        # self.attack_damage = 0 # This will not be used on the player because it will have a more complicated damage calculator
        # self.attack_variance = 1
        # self.crit = 5

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
        if DEBUG and DEBUG_STATE.stats:
            super().__init__(
                    _health=230,
                    _healthMax=230,
                    _stamina=50,
                    _staminaMax=50,
                    _strength=10,
                    _speed=120,
                    _attack_variance=1,
                    _attack_speed=400, # This is a delay in milliseconds
                    _defense=15,
                    _crit=5, # This is a percent out of 100 (make sure its an integer)
                    _critBonus = 200, # This is a percent
                    _sprint_multiplier = 2
                    )
        else:
            super().__init__(
                    _health=30,
                    _healthMax=30,
                    _stamina=50,
                    _staminaMax=50,
                    _strength=10,
                    _speed=30,
                    _attack_variance=1,
                    _attack_speed=400, # This is a delay in milliseconds
                    _defense=15,
                    _crit=5, # This is a percent out of 100 (make sure its an integer)
                    _critBonus = 200, # This is a percent
                    _sprint_multiplier = 2
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

    @property
    def health(self):
        return self._health

    @property
    def healthMax(self):
        return self._healthMax + self.player.inventory.get_buffs("healthMax")

    @property
    def stamina(self):
        return self._stamina

    @property
    def staminaMax(self):
        return self._staminaMax

    @property
    def strength(self):
        return self._strength + self.player.inventory.get_buffs("strength")

    @property
    def speed(self):
        return self._speed

    @property
    def attack_variance(self):
        return self._attack_variance

    @property
    def attack_speed(self):
        return self._attack_speed

    @property
    def defense(self):
        return self._defense

    @property
    def crit(self):
        return self._crit

    @property
    def critBonus(self):
        return self._critBonus

    @property
    def sprint_multiplier(self):
        return self._sprint_multiplier

