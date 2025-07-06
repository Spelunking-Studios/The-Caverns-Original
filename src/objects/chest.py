import pygame, pymunk
from src.stgs import asset, now
from src import util
from src import items


class Chest(util.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = [
            game.sprites,  # So the game will render it
            game.layer1,  # So the game will update it
            game.groups.colliders,  # So the player will collide
            game.groups.interactable  # So the player can interact with it
        ]
        super().__init__(self.groups)
        
        self.id = objT.id
        self.game_id = None

        for k, v in kwargs.items():
            self.__dict__[k] = v
        for k, v in objT.properties.items():
            self.__dict__[k] = v

        self.objT = objT
        self.rect = pygame.Rect(
            objT.x, objT.y,
            64, 64
        )
        self.image = pygame.image.load(asset("objects", "Chest.png"))
        self.last_interact = 0

        self.item = items.__dict__[self.item]
        
        self.opened = False
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = objT.x+32, objT.y+32
        self.shape = pymunk.Poly.create_box(self.body, (64, 64))
        self.shape.collision_type = 1
        self.shape.friction = 0.5
        self.game.space.add(self.body, self.shape)

        if not self.game_id:
            self.game_id = self.id
        
        if self.game_id in game.progress["chests_opened"]:
            self.opened = True

    def update(self):
        pass

    def interact(self):
        if now() - self.last_interact > 900:
            if self.opened:
                self.game.dialogueScreen.dialogueFromText("The chest is empty. . .")
            else:
                name = self.item.kind
                self.game.dialogueScreen.dialogueFromText(f"You find a {name}")
                self.game.player.inventory.add_item(self.item())
                self.game.progress["chests_opened"].append(self.game_id)
                self.opened = True
                self.game.toggleInventory()

            self.last_interact = now()
