from .effect import Effect
import pygame

class HurtEffect(Effect):
    """Generic hurt effect"""
    def __init__(self, game, referant, **kwargs):
        super().__init__(game, referant)
        self.duration = 0.25
        for key, value in kwargs.items():
            self.__dict__[key] = value
    def update(self):
        super().update()
        darkness = min(255, max(0, round(
            255 * (self.accumulator/self.duration)
        )))
        self.referant.image.fill(
            (255, darkness, darkness),
            special_flags = pygame.BLEND_MULT
        )
        super().checkForEnd()