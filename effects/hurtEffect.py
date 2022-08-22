from .effect import Effect
import pygame

class HurtEffect(Effect):
    """Generic hurt effect"""
    def __init__(self, sprite, **kwargs):
        super().__init__(sprite.game, sprite)
        self.duration = 0.25
        for key, value in kwargs.items():
            self.__dict__[key] = value
    def update(self):
        super().update()
        darkness = min(255, max(0, round(
            255 * (self.accumulator/self.duration)
        )))
        self.sprite.image.fill(
            (255, darkness, darkness),
            special_flags = pygame.BLEND_MULT
        )
        super().checkForEnd()