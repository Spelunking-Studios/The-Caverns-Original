import pygame, math
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
        self.updateRendTiles()
    def updateRendTiles(self):
        """Updates the rendTiles"""
        if self.rendUpdateCD > 0:
            self.rendUpdateCD -= 1
        # Create list of renderable tiles
        self.rendTilesHN = int(self.level.game.settings.windowSize[1] / 32) + 1
        self.rendTilesWN = int(self.level.game.settings.windowSize[0] / 32) + 1
        rendTilesList = []
        rendXTilesList = []
        rendYTilesList = []
        # Get X list
        # Left
        rx = 0
        remX = self.rendTilesWN / 2
        while remX >= 0 and rx <= self.focusedPoint[0]:
            rendXTilesList.append([rx, self.focusedPoint[1]])
            rx += 1
            remX -= 1
        # Right
        rx = self.focusedPoint[0] + 1
        remX = self.rendTilesWN / 2
        while remX >= 0 and rx <= self.size[0]:
            rendXTilesList.append([rx, self.focusedPoint[1]])
            rx += 1
            remX -= 1
        # Get Y list
        # Top
        ry = 0
        remY = self.rendTilesHN / 2
        while remY >= 0 and ry <= self.focusedPoint[1]:
            rendYTilesList.append([self.focusedPoint[1], ry])
            ry += 1
            remY -= 1
        # Bottom
        ry = self.focusedPoint[1] + 1
        remY = self.rendTilesHN / 2
        while remY >=0 and ry <= self.size[1]:
            rendYTilesList.append([self.focusedPoint[1], ry])
            ry += 1
            remY -= 1
        # Actually get the list of tiles
        for y in [u[1] for u in rendYTilesList]:
            for x in [u[0] for u in rendXTilesList]:
                rendTilesList.append([x, y])
        self.rendTiles = rendTilesList
        self.rendUpdateCD = 60
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
        # Update rendTiles
        self.updateRendTiles()
        # Update all rendTiles
        for tpos in self.rendTiles:
            t = self.findTileByPos(tpos)
            if t:
                t.update()
    def draw(self):
        """Draws the map"""
        if self.surface:
            # Draw all the tiles that will end up on the screen
            for tpos in self.rendTiles:
                t = self.findTileByPos(tpos)
                if t:
                    t.draw()
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