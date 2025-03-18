from items import Weapon

class Wand(Weapon):

    kind = "Wand"

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(asset(""))
        self.damage = 50 
        self.refresh = 200
        self.manaConsumption = 20
