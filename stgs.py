import os, sys
import pygame
import colors
import math

TITLE = "The Caverns"
LOADING_TEXT = [
    "A darkness has fallen upon this once beautiful land.",
    "What was once full of life is now permeated with the stench of death and decay",
    "Lake crystal clear and sky pure blue turned red by the smoke that chokes the air.",
    "Where there were once animals and people living in harmony,",
    "There are now only creatures of darkness plotting their evil machinations.",
    "Where there was once a great kingdon of dwarves, their halls filled with splendor,",
    "There is now only the remains of their dark and dusty halls..."
]
LOADING_SCREEN_SHOWN_BEFORE = False
DEBUG = False

#### Establishes file paths ####
try:
    PATH = sys._MEIPASS     # Tries to see if the project is built
except AttributeError:
    PATH = os.path.dirname(os.path.realpath(__file__))

# Path to the asset folder
ASSETSPATH = os.path.join(PATH, 'assets')

#### Gets file for saving settings in game. Every variable set here is default. Clearing the settings file should load everything as default. ####
if PATH == os.path.dirname(os.path.realpath(__file__)): #Checks if game is running from local path or has gamedata stored in appdata
    saveFile = os.path.join(PATH, 'save.p')
else:
    saveFile = os.path.join(os.getenv('APPDATA'), 'theCaverns', 'save.p') # Gets save file from appdata
    try:
        with open(saveFile, 'r') as b:
            b.close()       # Just Checks if the file exists
    except FileNotFoundError:
        os.mkdir(os.path.join(os.getenv('APPDATA'), 'theCaverns'))
print(saveFile)

#### Either centers the player no matter what (False) or doesn't scroll over the boundary of the level (True and preferred) ####
CAMLIMIT = True
SHOWFPS = True

#### FPS BOIS ####
FPS = 60

#### Volumes ####
musicVolume = 1
fxVolume = 1

#### Returns the asset's path ####
def asset(*args):
    '''Returns asset path given asset name'''
    global ASSETSPATH
    r = ASSETSPATH
    for arg in args:
        r = os.path.join(r, arg)
    return r

def sAsset(assetName):
    '''Returns sound path given sound name'''
    global ASSETSPATH

    return os.path.join(ASSETSPATH, 'sounds', assetName)

def fAsset(assetName):
    '''Returns font path given font name'''
    global ASSETSPATH

    return os.path.join(ASSETSPATH, 'fonts', assetName)

def tAsset(assetName):
    '''Returns Tiled file path given font name'''
    global ASSETSPATH

    return os.path.join(ASSETSPATH, 'Tiled', assetName)

# Custom Generated fonts
fgenedfs = {}

def fgen(fn, s):
    """Generate a custom font"""
    rn = fn + "-" + s
    if not fgenedfs[rn]:
        fgenedfs[rn] = pygame.font.Font(fAsset(fn), s)
    return fgenedfs[rn]

#### Establishes window size ####
winWidth, winHeight = 1280, 720
winFlags = pygame.HWSURFACE

iconPath = asset('logo.jpeg')

#### Anti-Aliasing on text ####
aalias = True

#### Defines what key binding is set for each action ####
keySet = {
    'start': pygame.K_s,
    'retry':[pygame.K_r],
    'toggleCam': pygame.K_o,
    'map': pygame.K_m,
    'interact':pygame.K_SPACE,
    'pRight': [pygame.K_RIGHT, pygame.K_d],
    'pLeft': [pygame.K_LEFT, pygame.K_a],
    'pUp': [pygame.K_UP, pygame.K_w],
    'pDown':[pygame.K_DOWN, pygame.K_s],
    'fullScreen': pygame.K_f,
    'pause': pygame.K_p
}

joystickDisabled = True
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())] 
joystickConnected = True if len(joysticks) > 0 else False
joystickEnabled = True if joystickConnected and not joystickDisabled else False

def checkJoysticks():
    '''
    STILL IN BETA TESTING
    '''

    global joystickEnabled
    joystickEnabled = True if joystickConnected and not joystickDisabled else False

def getJoy1():
    '''
    STILL IN BETA TESTING
    '''
    return joysticks[0] if len(joysticks) > 0 else False
#### Changes movement from flying to platforming ####
platformer = True

def checkKey(move):
    '''Handy Dandy class for checking the status of keys given a 
    a) keyword for the built in mapped buttons
    b) a list of pygame keys in which it returns true for any
    c) or just a single pygame key

    pygame key being pygame.K_a or pygame.K_UP'''
    keys = pygame.key.get_pressed()
    if isinstance(move, str):
        try:
            for k in keySet[move]:
                if keys[k]:
                    return True
        except TypeError:
            if keys[keySet[move]]:
                return True
    else:
        try:
            for k in move:
                if keys[k]:
                    return True
        except TypeError:
            if keys[move]:
                return True
    return False

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

# Loads all fonts if program is run indirectly
if __name__ != '__main__':
    fonts = {
        'title1': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 42),
        'main-title1': pygame.font.Font(fAsset('PixelLove.ttf'), 68),
        'subtitle1': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 37),
        '2': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 25),
        '3': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 28),
        'description1': pygame.font.Font(fAsset('PottaOne-Regular.ttf'), 24),
        'title2': pygame.font.Font(fAsset('PixelLove.ttf'), 40),
        'caption1': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 24),
        'effect1': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 18),
        'gameover': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 60),
        'victory': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 72),
        'menu1': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 15)
    }

def dist(vec1, vec2):
    '''Distance formula between two pygame Vectors'''
    dist1 = (vec1.x-vec2.x)**2
    dist2 = (vec1.y-vec2.y)**2
    return math.sqrt(dist1+dist2)

import pickle

def loadSave(file):
    '''Load save

    STILL IN BETA TESTING
    '''
    try:
        with open(file, 'rb') as f:
            data = pickle.load(f)
            items = list(data.items())
            for k, v in items:
                globals()[k] = v
        checkJoysticks()
    except FileNotFoundError:
        print("No Save File")

def saveData(file, game):
    '''Save game settings

    STILL IN BETA TESTING
    '''
    saveDict = {    # Each value must corresponde to a global variable in this file
        'musicVolume': game.mixer.musicVolume,
        'fxVolume': game.mixer.fxVolume,
        'aalias': game.antialiasing,
        'SHOWFPS': game.showFps,
        'joystickDisabled': game.joystickDisabled,
        "LOADING_SCREEN_SHOWN_BEFORE": game.loadingScreenShownBefore
    }
    with open(file, 'wb') as f:
        pickle.dump(saveDict, f)

def tGet(objT, strValue, default=False):
    '''Somewhat redundant function for forcing properties out of a Tiled object

    Takes: objT (Tiled object), strValue (keyword), default=False (customize default value)'''
    try:
        return objT.properties[strValue]
    except KeyError:
        return default

def now():
    '''Returns number of cycles that pygame has been ticking'''
    return pygame.time.get_ticks()