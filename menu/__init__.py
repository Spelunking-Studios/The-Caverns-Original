import pygame
from stgs import asset
from .button import Button
from .image import Image
from .menuItem import MenuItem
from .settingSlider import SettingSlider
from .text import Text

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