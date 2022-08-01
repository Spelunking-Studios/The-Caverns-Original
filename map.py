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
        self.focusedPoint = [20, 12]
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
        # Window sizes
        windowHeight = self.level.game.settings.windowSize[1]
        windowWidth = self.level.game.settings.windowSize[0]
        # Midlines
        hMidline = windowHeight / 2
        vMidline = windowWidth / 2
        # Size of map when drawn
        size = self.surface.get_rect()
        size = [size[2], size[3]]
        # Active Screen
        activeScreen = self.level.game.screenManager.activeScreen
        activeScreenRect = activeScreen.surface.get_rect()
        # Focus point
        fp = [v * 32 for v in self.focusedPoint]
        fp[0] += self.scrollAmt[0]
        fp[1] += self.scrollAmt[1]
        # Only calculate scrollign if map is bigger than screen
        if size[1] > activeScreenRect[3]:
            # Above the horizontal midline
            # And not at the top
            if fp[1] < hMidline and self.getPos()[1] < (windowHeight * 0.1):
                # Find amount past the midline
                amtPast = hMidline - fp[1]
                # Scroll to the midline
                self.scrollAmt[1] += amtPast
            # Below the horizontal midline
            # And not at bottom
            if fp[1] > hMidline and (self.getPos()[1] + size[1]) > (windowHeight - (windowHeight * 0.1)):
                # Find amount past the midline
                amtPast = fp[1] - hMidline
                # Scroll to the midlone
                self.scrollAmt[1] -= amtPast
        if size[0] > activeScreenRect[2]:
            # Left of vertical midline
            # And not at the left
            if fp[0] < vMidline and self.getPos()[0] < (windowWidth * 0.1):
                # Find amount past the midline
                amtPast = vMidline - fp[0]
                # Scroll to the left
                self.scrollAmt[0] += amtPast
            # Right of the vertival midline
            # And not at the right
            if fp[0] > vMidline and (self.getPos()[0] + size[0]) > (windowWidth - (windowWidth * 0.1)):
                # Find amount past the midline
                amtPast = fp[0] - vMidline
                # Scroll to the left
                self.scrollAmt[0] -= amtPast
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
        # Window size in tiles
        windowSizeTilesHor = int(self.level.game.settings.windowSize[0] / 32) + 1
        windowSizeTilesVert = int(self.level.game.settings.windowSize[1] / 32) + 1
        # Update tiles
        for col in self.tileMap:
            for tile in col:
                # Not in screen, don't update
                if not tile.isOnScreen():
                    continue
                tile.update()
    def draw(self):
        """Draws the map"""
        if self.surface:
            # Window size in tiles
            windowSizeTilesHor = int(self.level.game.settings.windowSize[0] / 32) + 1
            windowSizeTilesVert = int(self.level.game.settings.windowSize[1] / 32) + 1
            # Draw tiles
            for col in self.tileMap:
                for tile in col:
                    # Not in screen, don't draw
                    if not tile.isOnScreen():
                        continue
                    tile.draw()
            pygame.draw.rect(self.surface, (0, 255, 0),
                (
                    self.focusedPoint[0] * 32,
                    self.focusedPoint[1] * 32,
                    32, 32
                )
            )
            activeScreen = self.level.game.screenManager.activeScreen
            mapInScreenPos = self.getPos()
            # Blit it!!!
            activeScreen.surface.blit(self.surface, mapInScreenPos)
    def getPos(self):
        """Get the position of the map"""
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
        return mapInScreenPos
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