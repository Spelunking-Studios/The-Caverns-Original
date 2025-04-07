import pygame
from time import time
from stgs import asset
import util
from inventory import Inventory


class Chest(util.Sprite):
    def __init__(self, game, tiled_obj, **kwargs):
        self.game = game
        self.groups = [
            game.sprites,  # So the game will render it
            game.layer3,  # So the game will update it
            game.groups.colliders,  # So the player will collide
            game.groups.interactable  # So the player can interact with it
        ]
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in tiled_obj.properties.items():
            self.__dict__[k] = v

        self.tiled_obj = tiled_obj
        self.rect = pygame.Rect(
            tiled_obj.x, tiled_obj.y,
            64, 64
        )
        self.image = pygame.image.load(asset("objects", "Chest.png"))
        self.inventory = Inventory()
        self.last_interaction_time = 0
        self.inventory.deserialize(self.default_contents)

    def update(self):
        pass

    def interact(self):
        self.last_interaction_time = time()
        print("interacted!")
