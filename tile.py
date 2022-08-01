import pygame

class Tile:
    """Represents a single tile in the map"""
    def __init__(self, map, tileType, pos, metadata = {}):
        """Initialize the tile
        
        Arguments:
        -----
        map: Map
        tileType: string
            The tile type
        pos: tuple
            The position of the tile (x, y)
        metadata: dict = {}
            Tile metadata
        """
        self.map = map
        self.x = pos[0]
        self.y = pos[1]
        self.tileType = tileType
        if self.tileType in self.map.tileTypes.keys():
            self.surface = self.map.preloadTileImages[self.tileType]
        else:
            self.surface = pygame.Surface((32, 32))
            self.surface.fill((255, 255, 255))
    def update(self):
        """Update the tile"""
        self.draw()
    def draw(self):
        """Draw the tile"""
        self.map.surface.blit(self.surface, (self.x * 32, self.y * 32))
    def isOnScreen(self):
        """Determines if the tile is on the screen"""
        # The number of tiles that can fit on the screen
        tilesInWindowH = self.map.level.game.settings.windowSize[0] / 32
        tilesInWindowV = self.map.level.game.settings.windowSize[1] / 32
        # The focus point of the map
        fp = self.map.focusedPoint
        # Distance from the focused point
        distFFPX = abs(fp[0] - self.x)
        distFFPY = abs(fp[1] - self.y)
        # Is the distance on the x axis greater than the number of tiles
        # that can fit in the window horizontaly
        rtv = distFFPX < tilesInWindowH
        # Is the distance on the y axis greater than the number of tiles
        # that can fit in the window vertically
        rtv = rtv and (distFFPY < tilesInWindowV)
        return rtv