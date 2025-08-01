from src.stgs import *
from src import util

class Event(util.Sprite):
    def __init__(self, game, objT, **kwargs):
        self.game = game
        self.groups = game.sprites, game.layer1
        self.game_id = None
        self.id = objT.id
        self.triggered = False
        self.repeatable = False
        super().__init__(self.groups)
        
        self.dump(kwargs, objT.properties) 
        self.rect = pygame.Rect(objT.x, objT.y, objT.width, objT.height)

        if not self.game_id:
            self.game_id = self.game.map.floor.room.get_id() + "/" + str(self.id)
        
        if self.game_id in game.progress["events_triggered"]:
            self.triggered = True

    def update(self):
        if self.repeatable or not self.triggered:
            if self.rect.colliderect(self.game.player.rect):
                if not self.triggered:
                    self.trigger()
                    self.last_triggered = now()
            else:
                self.triggered = False    # This logic makes it act like a pressure plate
                # Can only be triggered again when you leave and come back

    def save(self):
        self.game.progress["events_triggered"].append(self.game_id)
    
    def trigger(self):
        self.triggered = True
        self.save()

    def draw(self, ctx, transform=None):
        pass

class DialogueEvent(Event):
    def trigger(self):
        self.game.dialogueScreen.dialogueFromText(self.text)
        super().trigger()

