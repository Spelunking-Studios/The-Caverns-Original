import pygame

class Effect(pygame.sprite.Sprite):
    """Base Effect class"""
    def __init__(self, game, referant, **kwargs):
        """Init"""
        super().__init__()
        self.game = game
        self.referant = referant
        # Note: effect durations are measured in seconds
        self.duration = 1
        self.accumulator = 0
        self.over = False
        for key, value in kwargs.items():
            self.__dict__[key] = value
    def update(self):
        """Update"""
        self.accumulator += self.game.dt()
    def checkForEnd(self):
        if self.accumulator > self.duration:
            self.accumulator = 0
            self.over = True
            self.kill()