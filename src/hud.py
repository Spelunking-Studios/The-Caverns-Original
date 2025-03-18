import util
import pygame
from stgs import *
import menu
from menu import createFrame
import overlay
import menu
import colors
from math import sin 

class Hud(util.Sprite):
    def __init__(self, game):
        self.groups = game.sprites, game.hudLayer
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
    def render(self):
        pass
    def update(self):
        self.render()

class StatHud(util.Sprite):
    def __init__(self, game, **kwargs):
        self.groups = game.sprites, game.hudLayer
        self.game = game
        # Set up some defaults
        self.tWidth, self.tHeight =  10, 8   # Width and height of StatHud
        self.tileSize = 32
        self.text = ''
        self.border = False # False if no border

        for k, v in kwargs.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.baseImage =  createFrame(self.tWidth, self.tHeight, 32, self.border) if self.border else createFrame(self.tWidth, self.tHeight)
        self.rect = pygame.Rect(winWidth-350, 40, self.tWidth*self.tileSize, self.tHeight*self.tileSize)
        self.render()

    def render(self):
        s = self.game.player.stats
        hp = "RGB(120,20,0)"+ str(int(s.health)) if s.health < s.healthMax/2.5 else int(s.health)
        newText = f"Health = {hp}\nStrength = {s.strength}\nSpeed = {s.speed}\nAttack Damage = {s.inventory.getCurrent().damage}\nCritical = {s.crit}%"
        if not newText == self.text:
            self.text = newText
            self.image = self.baseImage.copy()
            text = menu.Text('caption1', self.text, colors.white, True, (self.tileSize, self.tileSize), True, ((self.tWidth-2)*self.tileSize, (self.tHeight-2)*self.tileSize,))
            self.image.blit(text.image, text.pos)
            self.image.set_alpha(128)
        
    def update(self):
        self.render()

class SlotsHud(util.Sprite):
    def __init__(self, game, **kwargs):
        self.groups = game.sprites, game.hudLayer
        self.game = game
        self.slots = pygame.sprite.Group()
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Create the slots
        self.sheildSlot = SlotHud((10, 610))
        self.mainSlot1 = SlotHud((130, 610))
        self.mainSlot2 = SlotHud((250, 610))
        self.spellSlot1 = SlotHud((890, 610))
        self.spellSlot2 = SlotHud((1020, 610))
        self.spellSlot3 = SlotHud((1150, 610))

        # Add the slots
        self.slots.add(self.sheildSlot)
        self.slots.add(self.mainSlot1)
        self.slots.add(self.mainSlot2)
        self.slots.add(self.spellSlot1)
        self.slots.add(self.spellSlot2)
        self.slots.add(self.spellSlot3)
    def update(self):
        self.slots.update()

class SlotHud(util.Sprite):
    def __init__(self, pos, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos

        self.slotImg = pygame.image.load(asset("ui/weapon_slot.png"))
        self.slotScale = 3/5
        self.slotSize = pygame.Vector2(self.slotImg.get_size())*self.slotScale
        self.slotImg = pygame.transform.scale(self.slotImg, (int(self.slotSize.x), int(self.slotSize.y)))

        self.image = self.renderBase()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
    
    def renderBase(self):
        img = pygame.Surface(self.slotSize, pygame.SRCALPHA)
        img.blit(self.slotImg, (0, 0))
        return img
    
    def render(self):
        pass

    def update(self):
        self.render()

class HeathHud(Hud):
    def __init__(self, game):
        super().__init__(game)
        self.rect = pygame.Rect(400, 680, 450, 20)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.bgColor = colors.dark(colors.grey, 70)
        self.padX, self.padY = 4, 3
        self.render()

    def render(self):
        self.image.fill(self.bgColor)
        pygame.draw.rect(
            self.image,
            colors.green,#colors.light(colors.green, sin(pygame.time.get_ticks()*80)),
            (self.padX, self.padY, (self.rect.width-self.padX*2)*(self.game.player.stats.health/self.game.player.stats.healthMax), self.rect.height-self.padY*2),
            0,
            5
        )
    def update(self):
        self.render()

class SanityHud(Hud):
    def __init__(self, game):
        super().__init__(game)
        self.rect = pygame.Rect(400, 640, 450, 20)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.bgColor = colors.dark(colors.grey, 70)
        self.padX, self.padY = 4, 3
        # self.render()

        # self.image.fill(self.bgColor)
    def update(self):
        self.render()
    
    # Overrides the sprite draw to use pygame's draw functions
    def draw(self, ctx, transform=lambda rect:rect):
        pygame.draw.rect(
            ctx,
            self.bgColor,
            transform(self.rect),
        )
        x, y = self.rect.topleft
        rect = pygame.Rect(x + self.padX, y + self.padY, (self.rect.width-self.padX*2)*(self.game.player.stats.sanity/self.game.player.stats.sanityMax), self.rect.height-self.padY*2)
        pygame.draw.rect(
            ctx,
            colors.white,#colors.light(colors.green, sin(pygame.time.get_ticks()*80)),
            transform(rect),
            0,
            5
        )



# class InventoryHud(util.Sprite):
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
