import pygame
from tile import Tile

class Map:
    """Represents the game map"""
    def __init__(self, level):
        """Initialize the map
        
        Arguments:
        -----
        level: Level
        """
        self.level = level
        self.size = None
        self.tileTypes = {}
        self.preloadTileImages = {}
        self.tileMap = []
        self.surface = None
        self.focusedPoint = [5, 5]
        self.rendTiles = []
        self.rendUpdateCD = 60
        self.scrollAmt = [0, 0]
    def loadFromJSON(self, jdata):
        """Load the map from JSON data
        
        Arguments:
        -----
        jdata: dict
            The JSON level data
        """
        # Map Size
        self.size = jdata["map"]["size"]
        # Map surface
        self.surface = pygame.Surface((self.size[0] * 32, self.size[1] * 32))
        self.surface.fill((255, 0, 0))
        # Tile Types
        self.tileTypes = jdata["map"]["tileData"]["tileTypes"]
        self.tileTypeMap = jdata["map"]["tileData"]["tileTypeMap"]
        # Type preload images
        for tileType in self.tileTypes.keys():
            self.preloadTileImages[tileType] = pygame.image.load(
                self.tileTypes[tileType]
            )
        # Time map
        self.tileMap = [
            [0 for y in range(self.size[1])]
            for x in range(self.size[0])
        ]
        # Ensure the size of the map matches the data
        dataSize = [
            len(jdata["map"]["tiles"]["cols"]),
            len(jdata["map"]["tiles"]["cols"][0])
        ]
        if self.size[0] != dataSize[0] or self.size[1] != dataSize[1]:
            raise IndexError(f"Map size is not the same size as the data. Map: {self.size}, Data: {dataSize}")
        # Add the tiles
        colIndex = 0
        for col in jdata["map"]["tiles"]["cols"]:
            tileIndex = 0
            for tile in col:
                ctiled = jdata["map"]["tiles"]["cols"][colIndex][tileIndex]
                self.tileMap[colIndex][tileIndex] = Tile(
                    self,
                    self.tileTypeMap[str(ctiled["type"])],
                    (colIndex, tileIndex),
                    ctiled["metadata"]
                )
                tileIndex += 1
            colIndex += 1
        self.updateScroll()
    def updateScroll(self):
        """Updates the scroll"""
        windowHeight = self.level.game.settings.windowSize[1]
        windowWidth = self.level.game.settings.windowSize[0]
        hMidline = windowHeight / 2
        vMidline = windowWidth / 2
        fp = [v * 32 for v in self.focusedPoint]
        fp[0] += self.scrollAmt[0]
        fp[1] += self.scrollAmt[1]
        print(fp, [windowWidth, windowHeight])
        # Above the horizontal midline
        if fp[1] < hMidline:
            # Find amount past the midline
            amtPast = hMidline - fp[1]
            # Scroll to the midline
            self.scrollAmt[1] += amtPast
        # Below the horizontal midline
        if fp[1] > hMidline:
            # Find amount past the midline
            amtPast = fp[1] - hMidline
            # Scroll to the midlone
            self.scrollAmt[1] -= amtPast
    def update(self):
        """Updates the map"""
        # Check for focusedPoint change
        keyManager = self.level.game.keyManager
        mc = 5/23
        # W
        if keyManager.getKey(pygame.K_w):
            self.focusedPoint[1] -= mc
        # S
        if keyManager.getKey(pygame.K_s):
            self.focusedPoint[1] += mc
        # A
        if keyManager.getKey(pygame.K_a):
            self.focusedPoint[0] -= mc
        # D
        if keyManager.getKey(pygame.K_d):
            self.focusedPoint[0] += mc
        # Update scroll
        self.updateScroll()
        # Update tiles
        for col in self.tileMap:
            for tile in col:
                tile.update()
    def draw(self):
        """Draws the map"""
        if self.surface:
            # Draw tiles
            for col in self.tileMap:
                for tile in col:
                    tile.draw()
            pygame.draw.rect(self.surface, (0, 255, 0),
                (
                    self.focusedPoint[0] * 32,
                    self.focusedPoint[1] * 32,
                    32, 32
                )
            )
            # Draw FPS
            fpsFont = pygame.font.Font(
                self.level.game.fasset("YuseiMagic-Regular.ttf"),
                15
            )
            fpsSurf = fpsFont.render(
                "FPS: " + str(int(self.level.game.fps)),
                False,
                (255, 255, 255),
                (0, 0, 0)
            )
            fpsPos = [0, 0, fpsSurf.get_rect()[2], fpsSurf.get_rect()[3]]
            self.surface.blit(fpsSurf, fpsPos)
            activeScreen = self.level.game.screenManager.activeScreen
            mapInScreenPos = [0, 0]
            # Size of map when drawn
            size = self.surface.get_rect()
            size = [size[2], size[3]]
            # Size of the active screen
            activeScreenRect = activeScreen.surface.get_rect()
            # Center the map on the x axis
            if size[0] < activeScreenRect[2]:
                mapInScreenPos[0] = ((activeScreenRect[2] / 2) - (size[0] / 2))
            # Center the map on the y axis
            if size[1] < activeScreenRect[3]:
                mapInScreenPos[1] = ((activeScreenRect[3] / 2) - (size[1] / 2))
            mapInScreenPos[0] += self.scrollAmt[0]
            mapInScreenPos[1] += self.scrollAmt[1]
            # Blit it!!!
            activeScreen.surface.blit(self.surface, mapInScreenPos)
    def findTileByPos(self, pos):
        """Finds the tile at the given position
        
        Arguments:
        -----
        pos: list
            The position
        """
        for col in self.tileMap:
            for tile in col:
                if tile.x == pos[0] and tile.y == pos[1]:
                    return tile
        return None