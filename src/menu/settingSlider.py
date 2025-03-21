import pygame
import colors


class SettingSlider(pygame.sprite.Sprite):
    '''
    A menu object that acts as a basic slider that stores it's value as a percentage
    (use SettingSlider.getRatio())
    It renders itself using pygame draw methods and color values given as SettingSlider.colors
    '''

    def __init__(self, game, pos, **kwargs):
        self.game = game
        self.bgColor = (0, 0, 0, 0)
        #          line (normal)           Rect
        self.colors = (colors.orangeRed, colors.yellow, (255, 255, 255))
        self.clicked = False
        self.text = ''
        self.center = False

        self.groups = []  # These few lines are the lines for component objects
        self.addGroups = []
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.groups = self.groups + self.addGroups
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect((0, 0, 200, 60))
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.sliderRect = pygame.Rect((0, 0, 20, 10))
        self.sliderRect.centery = self.rect.height/2
        self.sliderRect.x = self.rect.width - self.sliderRect.width

    def reset(self):
        self.sliderRect = pygame.Rect(self.sliderRect)
        self.sliderRect.centery = self.rect.height/2
        self.sliderRect.x = self.rect.width - self.sliderRect.width

    def update(self):
        if self.clicked:
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
            else:
                self.sliderRect.x = min(
                    self.rect.right-self.sliderRect.width,
                    self.game.get_mouse_pos()[0]-self.sliderRect.width
                ) - self.rect.x
                self.sliderRect.x = max(0, self.sliderRect.x)
        else:
            self.checkClicked()

        self.render()

    def get_ratio(self):
        return self.sliderRect.x/(self.rect.width-self.sliderRect.width)

    def setRatio(self, percent):  # Set between 0 & 1
        self.sliderRect.x = (self.rect.width-self.sliderRect.width)*percent

    def render(self):
        self.image.fill(self.bgColor)
        pygame.draw.line(
            self.image,
            self.colors[1],
            (0, self.rect.height/2),
            (self.sliderRect.centerx, self.rect.height/2),
            4
        )
        pygame.draw.line(
            self.image,
            self.colors[0],
            (self.sliderRect.centerx, self.rect.height/2),
            (self.rect.width, self.rect.height/2),
            4
        )
        pygame.draw.rect(self.image, self.colors[2], self.sliderRect)

    def checkClicked(self):
        if pygame.mouse.get_pressed()[0]: 
            mouseRect = pygame.Rect(self.game.get_mouse_pos()[0], self.game.get_mouse_pos()[1], 1, 1)
            if mouseRect.colliderect(self.rect):
                self.clicked = True
