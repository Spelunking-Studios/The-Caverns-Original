import pygame
from stgs import *
import menu
import overlay
import colors

def createFrame(width, height, tileSize = 32, bPal = pygame.image.load(asset('objects/dPallette2.png'))):
    baseImage = pygame.Surface((width*tileSize, height*tileSize), pygame.SRCALPHA)
    borderPalette = bPal.convert_alpha()
    tWidth = int(baseImage.get_width()/tileSize)
    tHeight = int(baseImage.get_height()/tileSize)

    for x in range(0, tWidth-1):
        for y in range(0, tHeight-1):
            baseImage.blit(borderPalette, (x*tileSize, y*tileSize), (tileSize, tileSize, tileSize, tileSize))

    for x in range(1, tWidth-1): # Renders top, bottom tiles
        baseImage.blit(borderPalette, (x*tileSize, 0), (tileSize, 0, tileSize, tileSize))
        baseImage.blit(borderPalette, (x*tileSize, baseImage.get_height()-tileSize), (tileSize, tileSize*2, tileSize, tileSize))
    
    for y in range(1, tHeight-1): # Renders left, right tiles
        baseImage.blit(borderPalette, (0, y*tileSize), (0, tileSize, tileSize, tileSize))
        baseImage.blit(borderPalette, (baseImage.get_width()-tileSize, y*tileSize), (tileSize*2, tileSize, tileSize, tileSize))
                
    baseImage.blit(borderPalette, (0, 0), (0, 0, tileSize, tileSize))
    baseImage.blit(borderPalette, (baseImage.get_width()-tileSize, 0), (tileSize*2, 0, tileSize, tileSize))
    baseImage.blit(borderPalette, (0, baseImage.get_height()-tileSize), (0, tileSize*2, tileSize, tileSize))
    baseImage.blit(borderPalette, (baseImage.get_width()-tileSize, baseImage.get_height()-tileSize), (tileSize*2, tileSize*2, tileSize, tileSize))

    return baseImage.convert_alpha()

class StatHud(pygame.sprite.Sprite):
    def __init__(self, game, **kwargs):
        self.groups = game.sprites, game.hudLayer
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.tWidth = 10
        self.tHeight =  8
        self.tileSize = 32
        self.text = ''
        self.baseImage = createFrame(self.tWidth, self.tHeight)
        self.rect = pygame.Rect(winWidth-350, 40, self.tWidth*self.tileSize, self.tHeight*self.tileSize)
        self.render()

    def render(self):
        s = self.game.player.stats
        hp = "RGB(120,20,0)"+ str(s.health) if s.health < s.healthMax/2.5 else s.health
        newText = f"Health = {hp}\nStrength = {s.strength}\nSpeed = {s.speed}\nAttack Damage = {s.inventory.getCurrent().damage}\nCritical = {s.crit}%"
        if not newText == self.text:
            self.text = newText
            self.image = self.baseImage.copy()
            text = overlay.Text('6', self.text, colors.white, True, (self.tileSize, self.tileSize), True, ((self.tWidth-2)*self.tileSize, (self.tHeight-2)*self.tileSize,))
            self.image.blit(text.image, text.pos)
            self.image.set_alpha(128)
        
    def update(self):
        self.render()

class InventoryHud(pygame.sprite.Sprite):
    def __init__(self, game, **kwargs):
        self.groups = game.sprites, game.hudLayer
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.tWidth = 10
        self.tHeight =  8
        self.tileSize = 32
        self.text = ''
        self.baseImage = createFrame(self.tWidth, self.tHeight)
        self.rect = pygame.Rect(40, 40, self.tWidth*self.tileSize, self.tHeight*self.tileSize)
        self.render()

    def render(self):
        s = self.game.player.stats
        hp = "RGB(0, 120, 0)"+ s.health
        print(hp)
        newText = f"Health = {hp}\nStrength = {s.strength}\nSpeed = {s.speed}\nAttack Damage = {s.inventory.getCurrent().damage}\nCritical = {s.crit}%"
        if not newText == self.text:
            self.text = newText
            self.image = self.baseImage.copy()
            text = overlay.Text('6', self.text, colors.white, True, (self.tileSize, self.tileSize), True, ((self.tWidth-2)*self.tileSize, (self.tHeight-2)*self.tileSize,))
            self.image.blit(text.image, text.pos)
            self.image.set_alpha(128)
        
    def update(self):
        self.render()