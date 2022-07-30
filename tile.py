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
            self.surface = pygame.Surface((56, 56))
            self.surface.fill((255, 255, 255))
    def update(self):
        """Update the tile"""
        self.draw()
    def draw(self):
        """Draw the tile"""
        self.map.surface.blit(self.surface, (self.x * 65, self.y * 65))