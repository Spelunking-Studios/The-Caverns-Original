import pygame
from stgs import fonts
import colors

class Button(pygame.sprite.Sprite):
    '''
    A menu object that that stores a clicked value when hovered over

    Arguments
    |    Button.text [str] - stores optional text value
    |    Button.colors [tup] - Stores colors 
    |    Button.center [bool] - Stores whether text is centered or not

    Values
    |    Button.clicked [bool] - stores whether it has been clicked or ot since initiation
    |    Button.
    '''
    def __init__(self, game, pos,**kwargs):
        self.game = game
        
        self.onClick = False
        self.groups = []
        self.wh = (200, 60)
        self.colors = (colors.yellow, (255, 255, 255))
        self.spriteInit = False
        self.hover = False
        self.clicked = False
        self.instaKill = False
        self.text = ''
        self.center = True
        self.rounded = True
        self.textColors = (colors.black, colors.black)
        for k, v in kwargs.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(0, 0, 20, 20)
        self.rect.size = self.wh
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 0))
        self.setText(self.text)
    def setText(self, text, color = 0):
        """Sets the button's text
        
        Arguments:
        -----
        text: string,
        color: int = 0
            The index of the text color in the textColor array.
        """
        # Set the text
        self.text = text
        # Re-create the pygame surface with the text
        self.rendText = fonts['menu1'].render(
            self.text,
            self.game.antialiasing,
            self.textColors[color]
        )
        self.textRect = self.rendText.get_rect()
        if self.center:
            self.textRect.center = pygame.Rect(
                0, 0,
                self.rect.width, self.rect.height
            ).center
        else:
            self.textRect.x += 2
            self.textRect.y += 2
    def update(self):
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.hover = False
        self.clicked = False
        mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        if mouseRect.colliderect(self.rect):
            self.hover = True
        
        if self.hover:
            for event in self.game.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                    self.game.mixer.playFx('menu1')
                    if self.onClick:
                        self.onClick()
                        if self.instaKill:
                            self.kill()

        self.drawBG(int(self.hover))
        
        self.image.blit(self.rendText, self.textRect)
    def drawBG(self, colorIndex = 0):
        if self.rounded:
            borderRadius = 15
        else:
            borderRadius = 0
        pygame.draw.rect(
            self.image,
            self.colors[colorIndex],
            self.image.get_rect(),
            0,
            borderRadius
        )
        self.setText(self.text, colorIndex)
        return
    def reset(self):
        self.clicked = False