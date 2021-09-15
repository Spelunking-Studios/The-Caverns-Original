class Inventory():
	def __init__(self, master):
		self.spacesCount = 5
		self.spaces = []
		self.master = master
		for i in range(self.spacesCount):
			self.spaces.append({type: "void"})
	def setSpaceInfo(self, spaceNumber, item = {type:"void"}):
		if not spaceNumber > self.spacesCount:
			self.spaces[spaceNumber] = item
	def getSpaceInfo(self, spaceNumber):
		if not spaceNumber > self.spacesCount:
			return self.spaces[spaceNumber]
	def getInventoryInfo(self):
		index = {}
		index["master"] = self.master
		index["spacesCount"] = self.spacesCount
		index["spaces"] = self.spaces
		return index