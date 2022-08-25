import pygame
from stgs import winWidth, winHeight, asset, checkKey

class MapOverlay(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self, game.overlayer)
        self.components = pygame.sprite.Group()
        self.text = []
        self.active = False
        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.Surface((winWidth, winHeight), pygame.SRCALPHA).convert()
        self.loadComponents()
        self.render()

    def loadComponents(self):
        for comp in self.components:
            comp.kill()
            
        self.mapImage = pygame.image.load(asset('gameMap.png'))
        self.mapImage = pygame.transform.scale(self.mapImage, (int(winWidth), int(winHeight))).convert()

    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False

    def update(self):
        now = pygame.time.get_ticks()
        if self.active:
            self.render()
            self.components.update()
            if checkKey("map") and now - self.game.lastPause >= 180:
                self.deactivate()
                self.game.unPause()
                self.game.lastPause = now
        else:
            if checkKey("map") and now - self.game.lastPause >= 180:
                self.activate()
                self.game.pause = True
                self.game.lastPause = now
    
    def render(self):
        self.image.fill((0,0,0,190)) #self.transparent)
        self.image.blit(self.mapImage, (0, 0))
        # for comp in self.components:
        #     self.image.blit(comp.image, comp.rect)
        # for text in self.text:
        #     self.image.blit(text.image, text.pos) 