import os, sys
import pygame
import colors
import math

TITLE = "The Caverns"

#### Establishes file paths ####
try:
    PATH = sys._MEIPASS
except AttributeError:
    PATH = os.getcwd()

ASSETSPATH = os.path.join(PATH, 'assets')

#### Gets file for saving settings in game. Every variable set here is default. Clearing the settings file should load everything as default. ####
if PATH == os.getcwd(): #Checks if game is running from local path or has gamedata stored in appdata
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
def asset(assetName):
    global ASSETSPATH

    return os.path.join(ASSETSPATH, assetName)

def sAsset(assetName):
    global ASSETSPATH

    return os.path.join(ASSETSPATH, 'sounds', assetName)

def fAsset(assetName):
    global ASSETSPATH

    return os.path.join(PATH, 'fonts', assetName)

#### Establishes window size ####
winWidth, winHeight = 1280, 720
iconPath = asset('logo.png')
#### Anti-Aliasing on text ####
aalias = True

#### Defines what key binding is set for each action ####
keySet = {'start': pygame.K_s,'retry':[pygame.K_r], 'toggleCam': pygame.K_c, 'map': pygame.K_m, 'pRight': [pygame.K_RIGHT, pygame.K_d], 'pLeft': [pygame.K_LEFT, pygame.K_a], 'pUp': [pygame.K_UP, pygame.K_w], 'pDown':[pygame.K_DOWN, pygame.K_s],'fullScreen': pygame.K_f, 'pause': pygame.K_p}

#### Changes movement from flying to platforming ####
platformer = True

def checkKey(move):
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
    # utility class for loading and parsing spritesheets
    def __init__(self, filePath, *args):
        if len(args) > 0:
            if args[0]:
                self.image = filePath
            else:
                self.image = pygame.image.load(filePath)
        else:
            self.image = pygame.image.load(filePath)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        img = pygame.Surface((width, height), pygame.SRCALPHA)
        img.fill((0, 0, 0, 0))
        img.blit(self.image, (0, 0), (x, y, width, height))
        img = pygame.transform.scale(img, (width, height))
        return img

if not __name__ == '__main__':
    fonts = {'1': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 40),
            '2': pygame.font.SysFont('Comic Sans MS', 23),
            '3': pygame.font.Font(fAsset('PottaOne-Regular.ttf'), 32),
            '4': pygame.font.Font(fAsset('PottaOne-Regular.ttf'), 24),
            '5': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 60),
            '6': pygame.font.Font(fAsset('YuseiMagic-Regular.ttf'), 24),
            }

    
DEBUG = True ## Not much use right now. Can be used to control try/except statement flows.

def dist(vec1, vec2):
    dist1 = (vec1.x-vec2.x)**2
    dist2 = (vec1.y-vec2.y)**2
    return math.sqrt(dist1+dist2)

import pickle

def loadSave(file):
    try:
        with open(file, 'rb') as f:
            data = pickle.load(f)
            for k, v in data.items():
                globals()[k] = v
    except FileNotFoundError:
        print("No Save File")

def saveData(file, game):
    saveDict = {    # Each value must corresponde to a global variable in this file
        'musicVolume': game.mixer.musicVolume,
        'fxVolume': game.mixer.fxVolume,
        'aalias': game.antialiasing,
        'SHOWFPS': game.showFps,
    }
    with open(file, 'wb') as f:
        pickle.dump(saveDict, f)

def tGet(objT, strValue, default=False):
    try:
        return objT.properties[strValue]
    except KeyError:
        return default