from .enemy import Enemy

class RatBoss(Enemy):
    """Rat Boss enemy"""
    def __init__(self, game, objT):
        super().__init__(game, objT)
        self.health = 200
        self.damage = 5
        self.width = 64
        self.height = 64
        self.angle = 0
        self.speed = 60
        self.attackDelay = 240