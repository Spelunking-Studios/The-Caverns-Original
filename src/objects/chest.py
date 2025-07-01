import pygame
from src.stgs import asset, now
from src import util
from src import items


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
        self.last_interact = 0

        self.item = items.__dict__[self.item]
        
        self.opened = False

    def update(self):
        pass

    def interact(self):
        print("chest created")
        if now() - self.last_interact > 900:
            if self.opened:
                self.game.dialogueScreen.dialogueFromText("The chest is empty. . .")
            else:
                name = self.item.kind
                self.game.dialogueScreen.dialogueFromText(f"You find a {name}")
                self.opened = True

            self.last_interact = now()
