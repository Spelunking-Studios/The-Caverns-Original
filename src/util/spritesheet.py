import pygame

class Spritesheet:
    '''utility class for loading and parsing spritesheets'''

    def __init__(self, filePath):
        '''Takes a filepath or file'''

        try:
            self.image = pygame.image.load(filePath).convert_alpha()
        except TypeError:
            self.image = filePath.copy().convert_alpha()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def get_image(self, x, y, width, height):
        ''' Grabs an image out of the spritesheet image

        takes: x, y, width, height'''
        img = pygame.Surface((width, height), pygame.SRCALPHA)
        # img.fill((0, 0, 0, 0))
        img.blit(self.image, (0, 0), (x, y, width, height))
        img = pygame.transform.scale(img, (width, height))
        return img.convert_alpha()

