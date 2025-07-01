import pygame
from src import stgs
from src.menu import Text


class Tooltip:
    def __init__(self, title, desc, padding, title_font=stgs.fonts["title3"]):
        self.title = title
        self.desc = desc
        self.title_font = title_font
        self.desc_font = stgs.fonts["tooltip"]
        self.padding = padding
        self.maxToolTipSize = 300

    def render(self, target, offset_x, offset_y):
        # Render the title and desc
        title = self.title_font.render(self.title, stgs.aalias, stgs.colors.white)
        desc = Text(
            self.desc_font,
            self.desc,
            stgs.colors.white,
            stgs.aalias,
            multiline=True,
            size=(self.maxToolTipSize - self.padding * 2, 900)
        )

        # Determine the size of a box that we need
        width = self.maxToolTipSize
        height = title.get_height() + desc.last_rendered_y \
            + self.padding * 3  # 3 to account for padding between title and desc

        # Rendering time
        pygame.draw.rect(target, (40, 40, 40), (offset_x, offset_y, width, height))
        target.blit(title, (offset_x + self.padding, offset_y + self.padding))
        target.blit(
            desc.image,
            (offset_x + self.padding, offset_y + title.get_height() + self.padding)
        )
