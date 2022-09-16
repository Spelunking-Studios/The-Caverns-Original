import pygame

class Image(pygame.sprite.Sprite):
    """Basic Image"""
    def __init__(self, image, pos, **kwargs):
        if image:
            self.trueImage = image.copy()
            self.image = image
        else:
            self.trueImage = pygame.Surface((1, 1), pygame.SRCALPHA)
            self.trueImage.fill((0, 0, 0, 0))
            self.image = pygame.Surface((64, 64))
        self.colors = [(50, 50, 50), (60, 60, 60)]
        self.x = pos[0]
        self.y = pos[1]
        self.width = 32
        self.height = 32
        self.groups = []
        for key, value in kwargs.items():
            self.__dict__[key] = value
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        super().__init__(self.groups)
        self.drawBG()
    def drawBG(self, colorIndex = 0):
        self.image.fill(self.colors[colorIndex])
        self.image.blit(self.trueImage, (0, 0))
    def update(self):
        mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)