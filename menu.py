import pygame
import colors
from stgs import *

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
        #          Normal           Selected
        self.colors = (colors.yellow, (255, 255, 255))
        self.spriteInit = False
        self.hover = False
        self.clicked = False
        self.instaKill = False
        self.text = ''
        self.center = False
        for k, v in kwargs.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(0, 0, 20, 20)
        self.rect.size = self.wh
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.setText(self.text)
    def setText(self, text):
        """Sets the button's text
        
        Arguments:
        -----
        text: string
        """
        # Set the text
        self.text = text
        # Re-create the pygame surface with the text
        self.rendText = fonts['menu1'].render(
            self.text,
            self.game.antialiasing,
            (0, 0, 0)
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
        self.image = pygame.Surface(self.rect.size)
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

            self.image.fill(self.colors[1])
        else:
            self.image.fill(self.colors[0])
        
        self.image.blit(self.rendText, self.textRect)
    
    def reset(self):
        self.clicked = False

class Text:
    '''
    Basic Text object
    '''
    def __init__(self, fNum, text, color, aalias=True, pos=(0, 0), multiline=False, size=(900, 600), bgColor=(0, 0, 0, 0), ):
        if isinstance(fNum, str):
            self.font = fonts[fNum]
        else:
            self.font = fNum
        self.size = size
        self.color = color
        self.bgColor = bgColor
        self.pos = pygame.Vector2(pos)
        self.setText(text, multiline)
    def setText(self, text, multiline = False):
        if multiline:
            ## This code is thanks to https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame 
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            self.image.fill(self.bgColor)
            words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
            space = self.font.size(' ')[0]  # The width of a space.
            max_width, max_height = self.size
            x, y = 0, 0
            for line in words:
                for word in line:
                    if word  != '':
                        if word[0:3] == "RGB":
                            wordsplit = word[4:].split(')')
                            word_color = tuple([int(x) for x in wordsplit[0].split(',')])
                            word = wordsplit[1]
                        else:
                            word_color = self.color
                        word_surface = self.font.render(word, aalias, word_color)
                        word_width, word_height = word_surface.get_size()
                        if x + word_width >= max_width:
                            x = 0  # Reset the x.
                            y += word_height  # Start on new row.
                        self.image.blit(word_surface, (x, y))
                        x += word_width + space
                x = 0 # Reset the x.
                y += word_height  # Start on new row.
        else: 
            self.image = self.font.render(text, aalias, self.color)
        
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())
        self.image = self.image.convert_alpha()

class SettingSlider(pygame.sprite.Sprite):
    '''
    A menu object that acts as a basic slider that stores it's value as a percentage ( use SettingSlider.getRatio() )
    It renders itself using pygame draw methods and color values given as SettingSlider.color
    '''
    
    def __init__(self, game, pos,**kwargs):
        self.game = game
        self.rect = (0, 0, 200, 60)
        self.sliderRect = (0, 0, 20, 10)
        self.bgColor = colors.black
        #          line (normal)           Rect
        self.colors = (colors.orangeRed, colors.yellow, (255, 255, 255))
        self.clicked = False
        self.text = ''
        self.center = False

        self.groups = []       ## These few lines are the lines for component objects
        self.addGroups = []
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        self.groups = self.groups + self.addGroups
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(self.rect)
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size)
        self.sliderRect = pygame.Rect(self.sliderRect)
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
                self.sliderRect.x = min(self.rect.right-self.sliderRect.width, pygame.mouse.get_pos()[0]-self.sliderRect.width) - self.rect.x
                self.sliderRect.x = max(0, self.sliderRect.x)
        else:
            self.checkClicked()
        
        self.render()
    
    def get_ratio(self):
        return self.sliderRect.x/(self.rect.width-self.sliderRect.width)
    
    def setRatio(self, percent): # Set between 0 & 1
        self.sliderRect.x = (self.rect.width-self.sliderRect.width)*percent

    def render(self):
        self.image.fill(self.bgColor)
        pygame.draw.line(self.image, self.colors[1],(0, self.rect.height/2), (self.sliderRect.centerx, self.rect.height/2), 4)
        pygame.draw.line(self.image, self.colors[0],(self.sliderRect.centerx, self.rect.height/2), (self.rect.width, self.rect.height/2), 4)
        pygame.draw.rect(self.image, self.colors[2], self.sliderRect)

    
    def checkClicked(self):
        if pygame.mouse.get_pressed()[0]: 
            mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
            if mouseRect.colliderect(self.rect):
                self.clicked = True

class MenuItem(pygame.sprite.Sprite):
    '''
    A menu object that zooms in and out when hovered over. Requires a position and surface.
    
    Does not currently store whether it has been clicked or not, only serves as a basic object. 
    '''
    def __init__(self, game, pos, image, **kwargs):
        self.game = game
        self.rect = (0, 0, 180, 210)
        self.bgColor = (0, 0, 0, 0)
        #          line (normal)           Rect
        self.hover = False
        self.zoom = 1
        self.zoomMax = 2
        self.zoomMin = 1
        self.zoomSpeed = 0.4
        self.desc = ''
        self.text = ''
        self.groups = []       ## These few lines are the lines for component objects
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(self.rect)
        self.rect.topleft = pos
        self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        self.imageSrc = pygame.image.load(image)

    def setIcon(self):
        self.icon = pygame.transform.scale(self.imageSrc, (int(self.imageSrc.get_width()*self.zoom), int(self.imageSrc.get_height()*self.zoom)))
        
    def setRect(self):
        self.rect = self.imageSrc.get_rect()
    
    def render(self):
        self.image.fill(self.bgColor)
        self.setIcon()
        rect = self.icon.get_rect(center=(self.rect.w/2, self.rect.h/2))
        self.image.blit(self.icon, rect)
    
    def update(self):
        self.hover = False
        mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        if mouseRect.colliderect(self.rect):
            self.hover = True
        if self.hover:
            self.zoom = min(self.zoomMax, self.zoom + self.zoomSpeed)
        else:
            self.zoom = max(self.zoomMin, self.zoom - self.zoomSpeed)
        
        self.render()

def createFrame(width, height, tileSize = 32, bPal = pygame.image.load(asset('objects/dPallette2.png'))):
    '''
    Create a GUI frame from a 3x3 tile pallet provided a given width and height.
    NOTE: The height and width are refering to # in tiles
    '''
    baseImage = pygame.Surface((width*tileSize, height*tileSize), pygame.SRCALPHA)
    borderPalette = bPal.convert_alpha()
    tWidth = int(baseImage.get_width()/tileSize)
    tHeight = int(baseImage.get_height()/tileSize)

    for x in range(0, tWidth-1):
        for y in range(0, tHeight-1):
            baseImage.blit(borderPalette, (x*tileSize, y*tileSize), (tileSize, tileSize, tileSize, tileSize))

    for x in range(1, tWidth-1): # Renders top, bottom tiles
        baseImage.blit(borderPalette, (x*tileSize, 0), (tileSize, 0, tileSize, tileSize))
        baseImage.blit(borderPalette, (x*tileSize, baseImage.get_height()-tileSize), (tileSize, tileSize*2, tileSize, tileSize))
    
    for y in range(1, tHeight-1): # Renders left, right tiles
        baseImage.blit(borderPalette, (0, y*tileSize), (0, tileSize, tileSize, tileSize))
        baseImage.blit(borderPalette, (baseImage.get_width()-tileSize, y*tileSize), (tileSize*2, tileSize, tileSize, tileSize))
                
    baseImage.blit(borderPalette, (0, 0), (0, 0, tileSize, tileSize))
    baseImage.blit(borderPalette, (baseImage.get_width()-tileSize, 0), (tileSize*2, 0, tileSize, tileSize))
    baseImage.blit(borderPalette, (0, baseImage.get_height()-tileSize), (0, tileSize*2, tileSize, tileSize))
    baseImage.blit(borderPalette, (baseImage.get_width()-tileSize, baseImage.get_height()-tileSize), (tileSize*2, tileSize*2, tileSize, tileSize))

    return baseImage.convert_alpha()