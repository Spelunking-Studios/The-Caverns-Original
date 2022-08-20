import pygame
from random import randint
import objects

class Stats:
	def __init__(self, **kwargs):
		# This will be used to set default values for properties that can be used
		self.health = 0
		self.strength = 0 # This will become a modifier for damage
		self.speed = 0
		self.atkDamage = 0 # This will not be used on the player because it will have a more complicated damage calculator
		self.atkVariance = 1
		self.crit = 5

		for k, v in kwargs.items():
			self.__dict__[k] = v
	
	def setValues(self, **kwargs):
		for k, v in kwargs.items():
			self.__dict__[k] = v
	
	def attack(self):
		damage = randint(max(0, self.atkDamage-self.atkVariance), self.atkDamage+self.atkVariance)
		return damage
	
	def isDead(self):
		return bool(self.health <= 0)

class PlayerStats(Stats):
	def __init__(self):
		super().__init__(
			health=50,
			healthMax=40,
			strength=0,
			speed=15,
			atkDamage=0,
			atkVariance=1,
			atkSpeed=400, # This is a delay in milliseconds
			crit=5, # This is a percent out of 100 (make sure its an integer)
			critBonus = 200, # This is a percent
		)
		self.inventory = Inventory(objects.Sword1(),  objects.MagicWand())
	
	def attack(self): # The index here just means which hotbar number the action is
		dmg = self.inventory.getCurrent().damage + self.strength/5
		atkVar = self.atkVariance + self.inventory.getCurrent().atkVariance
		if randint(0, 100) <= self.crit:
			crit = True
			damage = randint(max(0, int((dmg-atkVar)*(self.critBonus/100))), int((dmg+atkVar)*(self.critBonus/100)))
			print("DAMN YOU HIT A CRITICAL")
		else:
			crit = False
			damage = randint(max(0, dmg-atkVar), dmg+atkVar)
		
		return damage, crit

# zomb = Stats(atkDamage=3)
# print(zomb.attack())
	
class Inventory:
	def __init__(self, *args, **kwargs):#sprite, *args, **kwargs):
		self.slotMax = 5
		self.slots = {}
		self.slotFocus = 1
		#self.sprite = sprite
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
		for k,v in self.slots.items():
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

# inv1 = Inventory("banana", "apple", "strawberry", "coconut", "kiwi", "grape", slotMax = 6)
# inv1.setSlot(2, 'pineapple')
# print(inv1.slots)
# inv1.expand(2, 'peach', 'watermelon')
# print(inv1.slots)
# print(inv1.getIndex('peach'))