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
        self.surface = pygame.Surface((self.size[0] * 65, self.size[1] * 65))
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
        colIndex = 0
        for col in jdata["map"]["tiles"]["cols"]:
            tileIndex = 0
            ctiled = jdata["map"]["tiles"]["cols"][colIndex][tileIndex]
            for tile in col:
                self.tileMap[colIndex][tileIndex] = Tile(
                    self,
                    self.tileTypeMap[str(ctiled["type"])],
                    (colIndex, tileIndex),
                    ctiled["metadata"]
                )
                tileIndex += 1
            colIndex += 1
    def update(self):
        """Updates the map"""
        # Update all tiles in the map
        for col in self.tileMap:
            for tile in col:
                tile.update()
    def draw(self):
        """Draws the map"""
        if self.surface:
            # Draw all tiles in the map
            for col in self.tileMap:
                for tile in col:
                    tile.draw()
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