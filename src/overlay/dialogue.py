from src import util
import pygame
from src.stgs import winWidth, winHeight, checkKey, asset, fonts
from src.menu import createFrame
import src.util.colors as colors


class DialogueOverlay(util.Sprite):
    def __init__(self, game):
        self.game = game
        self.fade_in_time = 1400
        super().__init__( game.overlayer)
        self.components = pygame.sprite.Group()
        self.text = []
        self.active = True
        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.Surface(
            (winWidth, winHeight),
            pygame.SRCALPHA
        ).convert_alpha()
        self.load_components()
        self.render()
        self.lastInteract = pygame.time.get_ticks()

    def load_components(self):
        self.components = pygame.sprite.Group()

    def activate(self):
        self.active = True
        self.lastInteract = pygame.time.get_ticks()
        self.game.pause = True
        self.game.lastPause = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.lastInteract = pygame.time.get_ticks()
        self.game.pause = False
        self.game.lastPause = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        comp_len = len(self.components.sprites())
        if self.active:
            self.render()
            if comp_len == 0:
                self.deactivate()
            else:
                self.components.update()
                if checkKey("interact") and now-self.lastInteract > 200:
                    last_spr = self.components.sprites()[comp_len - 1]
                    if last_spr.finished:
                        for comp in self.components:
                            comp.kill()
                        self.deactivate()
        else:
            pass

    def render(self):
        self.image.fill((0,0,0,0))
        for comp in self.components:
            comp.draw(self.image)

    def dialogueFromNpc(self, npc):
        self.activate()
        self.components.add(Dialogue(self.game, npc.text))

    def dialogueFromText(self, text):
        self.activate()
        text = [text] if isinstance(text, str) else text
        for t in text:
            self.components.add(Dialogue(self.game, t))

    def draw(self, ctx, transform = None):
        super().draw(ctx, transform)

class Dialogue(util.Sprite):
    def __init__(self, game, text, **kwargs):
        self.groups = game.sprites
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.height = 8
        self.tileSize = 32
        self.scale = 0
        self.text = text
        self.rect = pygame.Rect(
            0, winHeight - self.height * self.tileSize,
            winWidth, self.height * self.tileSize
        )
        self.fade_in_time = 200
        self.textColor = colors.white
        self.lastInteract = pygame.time.get_ticks()
        self.aalias = True
        self.borderPalette = asset('objects/dialog-frame.png')
        # border_palette_size = (
        #     self.borderPalette.get_width() / self.tileSize,
        #     self.borderPalette.get_height() / self.tileSize
        # )
        # if any([i < 3 for i in border_palette_size]):
        #     print("Check your pallette size. It is currently invalid for the  set tile size.")  # noqa
        self.render()
        self.finished = False

    def render(self):
        self.image = pygame.Surface(
            (winWidth, self.height * self.tileSize),
            pygame.SRCALPHA
        )
        self.baseImage = createFrame(winWidth/self.tileSize, self.height, self.tileSize, self.borderPalette)
        self.rendText = DialogueText(
            'dialogue',
            self.text,
            (105, 125, 128),
            False,
            (self.tileSize, self.tileSize),
            (
                int(self.image.get_width() - self.tileSize * 2),
                int(self.image.get_height() - self.tileSize * 2)
            )
        )
        self.baseImage.convert_alpha()
        self.image.blit(self.baseImage, (0, 0))
        self.render_text()
        self.image.convert_alpha()

    def render_text(self):
        self.image.blit(self.rendText.get_current(), self.rendText.pos)

    def refresh(self):
        self.image = self.baseImage
        self.render_text()

    def update(self):
        now = pygame.time.get_ticks()

        # Little zoom in effect
        diff = now - self.lastInteract
        if diff < self.fade_in_time:
            self.scale = round(diff/self.fade_in_time, 2)
        else:
            self.scale = 1

        # The actual 
        if len(self.rendText.images) > 1:
            
            if checkKey("interact") and diff > 200:
                if self.rendText.index+1 >= len(self.rendText.images):
                    self.finished = True
                else:
                    self.rendText.index += 1
                self.refresh()
                self.lastInteract = now
        else:
            self.finished = True

    def draw(self, ctx, transform=None):
        if self.scale != 1:
            temp = self.image.copy()
            self.image = pygame.transform.scale_by(self.image, self.scale)
            self.rect = self.image.get_rect(center=self.rect.center)
            super().draw(ctx, transform)
            self.image = temp.copy()
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            super().draw(ctx, transform)


class DialogueText:
    def __init__(self,
                 fnum,
                 text,
                 color,
                 aalias=True,
                 pos=(0, 0),
                 size=(900, 600),
                 bg_color=(0, 0, 0, 0)):

        self.fnum = fnum
        self.text = text
        self.color = color
        self.aalias= aalias
        self.pos = pos
        self.size = size
        self.bg_color = bg_color
        # This code is thanks to
        # https://stackoverflow.com/questions/42014195/
        # rendering-text-with-multiple-lines-in-pygame.
        self.render()
        self.pos = pygame.Vector2(pos)

        self.rect = (self.pos.x, self.pos.y, size[0], size[1])
        for img in self.images:
            img.convert_alpha()

    def get_current(self):
        return self.images[self.index]

    def render(self):
        self.images = [pygame.Surface(self.size, pygame.SRCALPHA)]
        self.index = 0
        self.get_current().fill(self.bg_color)
        
        pad_y = 8

        font = fonts[self.fnum]
        # 2D array where each row is a list of words.
        words = [word.split(' ') for word in self.text.splitlines()]
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.size
        x, y = 0, 0
        for line in words:
            for word in line:
                if word != '':
                    word_surface = font.render(word, self.aalias, self.color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        # Check if rows overflow
                        x = 0  # Reset the x.
                        y += word_height + pad_y  # Start on new row.
                    if y > max_height - word_height:
                        # Check if text overflows from box
                        # (creates new box)
                        x, y = 0, 0
                        self.images.append(
                            pygame.Surface(self.size, pygame.SRCALPHA)
                        )
                        self.index += 1
                        self.get_current().convert_alpha()
                        self.get_current().fill(self.bg_color)
                    self.get_current().blit(word_surface, (x, y))
                    x += word_width + space
        self.index = 0

    def __str__(self):
        return self.image
