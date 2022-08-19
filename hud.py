import pygame
from stgs import *
import menu
from menu import createFrame
import overlay
import colors

class Hud(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.sprites, game.hudLayer
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
    def render(self):
        pass
    def update(self):
        self.render()

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
            text = overlay.Text('caption1', self.text, colors.white, True, (self.tileSize, self.tileSize), True, ((self.tWidth-2)*self.tileSize, (self.tHeight-2)*self.tileSize,))
            self.image.blit(text.image, text.pos)
            self.image.set_alpha(128)
        
    def update(self):
        self.render()

# The HUD for the current items in use
class SlotHud(pygame.sprite.Sprite):
    def __init__(self, game, **kwargs):
        self.groups = game.sprites, game.hudLayer
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.slotImg = pygame.image.load(asset("ui/weapon_slot.png"))
        self.slotScale = 4/5
        self.slotSize = pygame.Vector2(self.slotImg.get_size())*self.slotScale
        self.slotImg = pygame.transform.scale(self.slotImg, (int(self.slotSize.x), int(self.slotSize.y)))

        self.image = self.renderBase()
        self.rect = pygame.Rect(10, 8, self.image.get_width(), self.image.get_height())
    
    def renderBase(self):
        img = pygame.Surface((400, 200), pygame.SRCALPHA)
        img.blit(self.slotImg, (0, 0))
        img.blit(self.slotImg, (self.slotSize.x + 10, 0))
        return img
    
    def render(self):
        pass

    def update(self):
        self.render()

class HeathHud(Hud):
    def __init__(self, game):
        super().__init__(game)
        self.image = pygame.Surface((100, 20))
        self.image.fill((255, 255, 255))
        self.rect = pygame.Rect(20, 600, 100, 20)
        self.rendWidth = 100
    def render(self):
        self.image.fill((255, 255, 255))
        pygame.draw.rect(
            self.image,
            (255, 0, 0),
            (0, 0, self.rendWidth, 20)
        )
    def update(self):
        self.rendWidth = 100 / (50 / self.game.player.stats.health)
        self.render()

# class InventoryHud(pygame.sprite.Sprite):
#     def __init__(self, game, **kwargs):
#         self.groups = game.sprites, game.hudLayer
#         self.game = game
#         pygame.sprite.Sprite.__init__(self, self.groups)
        
#         self.tWidth = 10
#         self.tHeight =  8
#         self.tileSize = 32
#         self.text = ''
#         self.baseImage = createFrame(self.tWidth, self.tHeight)
#         self.rect = pygame.Rect(40, 40, self.tWidth*self.tileSize, self.tHeight*self.tileSize)
#         self.render()

#     def render(self):
#         s = self.game.player.stats
#         hp = "RGB(0, 120, 0)"+ s.health
#         print(hp)
#         newText = f"Health = {hp}\nStrength = {s.strength}\nSpeed = {s.speed}\nAttack Damage = {s.inventory.getCurrent().damage}\nCritical = {s.crit}%"
#         if not newText == self.text:
#             self.text = newText
#             self.image = self.baseImage.copy()
#             text = overlay.Text('caption1', self.text, colors.white, True, (self.tileSize, self.tileSize), True, ((self.tWidth-2)*self.tileSize, (self.tHeight-2)*self.tileSize,))
#             self.image.blit(text.image, text.pos)
#             self.image.set_alpha(128)
        
#     def update(self):
#         self.render()