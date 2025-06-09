import util
import pygame
from stgs import *
import menu
from menu import createFrame
import overlay
import menu
import src.util.colors as colors
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
        self.tWidth, self.tHeight =  10, 6   # Width and height of StatHud
        self.tileSize = 32
        self.text = ''
        self.border = True# False if no border

        for k, v in kwargs.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.baseImage =  createFrame(self.tWidth, self.tHeight, 32, self.border) if self.border else createFrame(self.tWidth, self.tHeight)
        self.rect = pygame.Rect(winWidth-350, 40, self.tWidth*self.tileSize, self.tHeight*self.tileSize)
        self.render()

    def render(self):
        s = self.game.player.stats
        hp = "RGB(120,20,0)"+ str(int(s.health)) if s.health < s.healthMax/2.5 else int(s.health)
        newText = f"Health = {hp}\nStrength = {s.strength}\nSpeed = {s.speed}\nAttack Damage = {self.game.player.slot1.damage}\nCritical = {s.crit}%"
        if not newText == self.text:
            self.text = newText
            self.image = self.baseImage.copy()
            text = menu.Text('caption1', self.text, (105, 125, 128), True, (self.tileSize, self.tileSize), True, ((self.tWidth-2)*self.tileSize, (self.tHeight-2)*self.tileSize,))
            self.image.blit(text.image, text.pos)
            self.image.set_alpha(128)
        
    def update(self):
        self.render()

class SlotsHud(Hud):
    def __init__(self, game, **kwargs):
        self.game = game
        self.slots = pygame.sprite.Group()
        super().__init__(game)

        # Create the slots
        self.slot1 = SlotHud((10, 610), scale=0.6)
        self.slot2 = SlotHud((130, 610), img_path = asset("ui/magic_slot.png"), scale = 0.64)

        self.healthHud = HeathHud(game, x = self.slot2.rect.right + 15)# + winWidth/2.5)
        self.sanityHud = SanityHud(game, x = self.slot2.rect.right + 15)# + winWidth/2.5)

        # Add the slots
        self.slots.add(self.slot1)
        self.slots.add(self.slot2)

    def update(self):
        self.slots.update()

    def draw(self, ctx, transform=None):
        
        for slotHud in self.slots:
            ctx.blit(slotHud.image, slotHud.rect)

        # draw items in slots
        size = pygame.math.Vector2(self.slot1.rect.size) #* 0.75
        # img1 = pygame.transform.scale(self.game.player.slot1.renderable, size)
        img1 = self.game.player.slot1.renderable
        ctx.blit(img1, (
            self.slot1.rect.left + size[0] * 0.18,
            self.slot1.rect.top + size[1] * 0.17
        ))
        ctx.blit(self.game.player.slot2.renderable, (
            self.slot2.rect.left + size[0] * 0.18,
            self.slot2.rect.top + size[1] * 0.17
        ))

class SlotHud(util.Sprite):
    def __init__(self, pos, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.img_path = asset("ui/armor_slot.png")
        self.scale = 1
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.pos = pos

        self.slotImg = pygame.image.load(self.img_path)
        self.slotSize = pygame.Vector2(self.slotImg.get_size())*self.scale
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
    """Good 'ol healthbar
    """

    def __init__(self, game, **kwargs):
        self.x, self.y = 400, 640
        for k,v, in kwargs.items():
            self.__dict__[k] = v
        
        self.pos = (self.x, self.y)
        super().__init__(game)
        self.rect = pygame.Rect(*self.pos, 450, 20)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.bgColor = colors.deep_slate
        self.padX, self.padY = 4, 3
        self.render()

    def render(self):
        self.image.fill(self.bgColor)
        percent =  self.game.player.stats.health/self.game.player.stats.healthMax
        color = colors.moss_green
        glow_range = 5
        if percent < 0.3:
            color = colors.vintage_wine    
            glow_range = 30
        pygame.draw.rect(
            self.image,
            colors.light(color, sin(pygame.time.get_ticks()/100)*glow_range),
            (self.padX, self.padY, (self.rect.width-self.padX*2)*(percent), self.rect.height-self.padY*2),
            0,
            5
        )
    def update(self):
        self.render()

class SanityHud(Hud):
    def __init__(self, game, **kwargs):
        self.x, self.y = 400, 680
        for k,v, in kwargs.items():
            self.__dict__[k] = v
        self.pos = (self.x, self.y)
        super().__init__(game)
        self.rect = pygame.Rect(*self.pos, 450, 20)
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
