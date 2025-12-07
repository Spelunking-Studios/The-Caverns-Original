import pygame
from src.stgs import *
from .item import Item

class Note(Item):
    kind = "Note"

    def __init__(self, text="The note is blank"):
        super().__init__()
        self.cache_key = "renderable__" + self.__class__.__name__
        self.stats['categories'] = self.base_categories + ["note"]
        self.stats['description'] = text
        self.set_image(
            asset("items", "note.png")
        )
        self.stats['text'] = text

    def get_text(self, cipher=False):
        # Adding the cipher parameter for future use
        return self.stats['text']
