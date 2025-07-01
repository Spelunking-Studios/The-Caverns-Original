import pygame
from src.stgs import aalias, fonts


class Text(pygame.sprite.Sprite):
    '''
    Text object with multiline support
    '''

    def __init__(self, fNum, text, color, aalias=True, pos=(0, 0), multiline=False, size=(900, 600), bgColor=(0, 0, 0, 0), **kwargs):
        if isinstance(fNum, str):
            self.font = fonts[fNum]
        else:
            self.font = fNum
        self.size = size
        self.color = color
        self.bgColor = bgColor
        self.pos = pygame.Vector2(pos)
        self.aalias = aalias
        self.groups = []

        for key, value in kwargs.items():
            self.__dict__[key] = value

        super().__init__(self.groups)

        self.setText(text, multiline)

    def setText(self, text, multiline=False):
        if multiline:
            # This code is thanks to https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame 
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            self.image.fill(self.bgColor)
            words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
            space = self.font.size(' ')[0]  # The width of a space.
            max_width, max_height = self.size
            x, y = 0, 0
            for line in words:
                for word in line:
                    if word != '':
                        if word[0:3] == "RGB":
                            wordsplit = word[4:].split(')')
                            word_color = tuple([int(x) for x in wordsplit[0].split(',')])
                            word = wordsplit[1]
                        else:
                            word_color = self.color
                        word_surface = self.font.render(word, self.aalias, word_color)
                        word_width, word_height = word_surface.get_size()
                        if x + word_width >= max_width:
                            x = 0  # Reset the x.
                            y += word_height  # Start on new row.
                        self.image.blit(word_surface, (x, y))
                        x += word_width + space
                x = 0  # Reset the x.
                y += word_height  # Start on new row.

            self.last_rendered_y = y
        else:
            self.image = self.font.render(text, aalias, self.color)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())
        self.image = self.image.convert_alpha()
