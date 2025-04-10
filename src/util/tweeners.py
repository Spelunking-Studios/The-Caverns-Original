import pytweening

class TweenManager:
    def __init__(self) -> None:
        self.tweens = []

    def update(self, dt):

        for t in self.tweens:
            t.update(dt)

        self.remove_tweens()

    def remove_tweens(self):
        for t in self.tweens.copy():

