import pygame, pymunk
import math
from src.stgs import asset, now
from src import util
from src.util import LightSource
from src.fx import SlowGlowParticles

class SavePoint(util.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = [
            game.sprites,
            game.layer1,  
            game.groups.interactable  # So the player can interact with it
        ]
        super().__init__(self.groups)
        
        self.last_interact = 0
        self.saved = False
        self.id = objT.id

        self.dump(kwargs, objT.properties) 
        self.objT = objT
        self.rect = pygame.Rect(
            0, 0,
            64, 64
        )
        self.rect.center = objT.x, objT.y
        self.image = pygame.image.load(asset("objects", "campfire.png"))

        self.smoke_particles = None
        self.light = None
        self.light_flicker_speed = 0.007
        self.light_base_power = 0.94
        self.lit = False

        self.location = "save-room1"

    def get_save_quotes(self):
        quotes = [
            "You light the abandon campfire. Its iridescence feels your soul with determination"
        ]
        return quotes[0]

    def update(self):
        if self.light:
            self.light.power = self.light_base_power + math.sin(now()*self.light_flicker_speed)*0.02
        pass

    def interact(self):
        if now() - self.last_interact > 900:
            if self.saved:
                self.game.dialogueScreen.dialogueFromText(self.get_save_quotes())
            else:
                self.game.dialogueScreen.dialogueFromText("You saved the game")
                self.game.progress["save_point"] = self.location
                self.light = LightSource(self.game, self.objT, power=self.light_base_power, color = util.colors.amber, radius=800)
                self.smoke_particles = SlowGlowParticles(
                    self.game, 
                    speed = 0.8,
                    bright=True,
                    color = util.colors.peach_rose
                )
                self.smoke_particles.position = self.rect.center
                self.saved = True

            self.last_interact = now()
