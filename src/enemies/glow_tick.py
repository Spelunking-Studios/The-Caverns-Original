from src.enemies.enemy import SimpleEnemy
from src.animations import Animator, HurtFx
from src.stgs import *

class GlowTick(SimpleEnemy):

    def __init__(self, game, objT, **kwargs):
        super().__init__(game, objT, **kwargs)

        self.animations = Animator({
            "default": asset("enemies/glow tick/glow_tick.png")
        })

    def update(self):
        super().update()

    def move (self):
        pass

    def draw(self, ctx, transform=None):
        self.image = self.animations.get_image()
        return super().draw(ctx, transform)
