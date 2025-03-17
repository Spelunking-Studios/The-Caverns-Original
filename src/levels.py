# from xml.dom.pulldom import parseString
import pygame
import pytmx
from stgs import *
import enemies
import objects as objs
import os

class GameMap:
    def __init__(self, game, index=2):
        self.game = game
        self.floors = [
            Floor(game, "Floor1"),
            Floor(game, "Floor2"),
            Floor(game, "Floor3"),
        ]
        self.index = index
        self.floor = self.floors[self.index]    # The floor loading will be based on an index within the floors list 

    def loadFloor(self, num=None):
        """Sets the map's floor and activates it"""
        self.floor = self.floors[num if num else self.index]
        self.floor.load()
    
    def switchRoom(self, room, startObj):
        for s in self.floor.room.sprites:
            s.kill()
        
        self.game.groups.killAll()
            
        self.floor.enterRoom(room, startObj)
    
    def getRoom(self):
        return self.floor.room
    
    def nextFloor(self):
        self.index += 1
        self.loadFloor()
    
    # def update(self):
    #     """Update the map"""
    #     self.floor.update()

class Floor:
    """Represents a floor"""
    def __init__(self, game, folder="Floor1"):
        """Basic initialization of props"""
        self.game = game
        self.folderPath = tAsset(folder)
        # Finds the path of every room in the floor folder
        self.roomPaths =  []
        for item in os.listdir(self.folderPath):
            f = os.path.join(self.folderPath, item)
            if os.path.isfile(f):
                self.roomPaths.append(f) 
        
        # print(self.roomPaths)
        # Generates room objects from path
        self.rooms = [Room(self, i) for i in self.roomPaths]
        # This stores the current room number or index within the rooms list 
        self.current = 0

    def load(self):
        """Loads the floor (by default in the first room)"""
        self.enterRoom("room1")

    def getRoomByName(self, name):
        for r in self.rooms:
            if r.name == name:
                return r
        raise Exception(f"NO ROOM CORRESPONDING TO {name}")

    def enterRoom(self, room, startObj="Entrance"):
        self.room = self.getRoomByName(room)
        self.room.load(startObj)

    # def clear(self):
    #     pass

    # def update(self):
    #     """Update the floor"""
    #     self.room.update(

class Room:
    """Represents a single room"""
    def __init__(self, floor, filePath, **kwargs):
        """Initialize the room"""
        self.floor = floor
        self.game = floor.game
        self.filePath = filePath
        self.scale = 2

        # Container for all the sprites corresponding to the room
        self.sprites = pygame.sprite.Group()
        # A way to track which sprite the player should go to when the room loads
        self.startSprite = None

        self.loaded = False
        # Gets the name from the file name. Not in use yet
        self.name = os.path.splitext(os.path.basename(self.filePath))[0]

        for k, v in kwargs.items():
            self.__dict__[k] = v

    def load(self, start="Entrance"):
        '''load the data for the room when the player enters it (replaces Ben's enter and load function)'''
        self.clearSprites()
        self.points = 0
        self.loadTiled(start)
        if self.startSprite:
            self.game.player.setPos(self.startSprite.rect.center, True)
        else:
            print("There is no starting object")
            self.game.player.setPos((self.width/2, self.height/2))

    def loadTiled(self, start="Entrance"):
        """Load data from the tiled file"""
        print(f"Loading {self.filePath}")
        self.tiledData = pytmx.load_pygame(self.filePath, pixelAlpha = True)
        self.width = self.tiledData.width * self.tiledData.tilewidth * self.scale
        self.height = self.tiledData.height * self.tiledData.tileheight * self.scale
        self.levelSize = (self.width, self.height)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.image = pygame.Surface(self.levelSize)
        for layer in self.tiledData.visible_layers:
            # Go through every layer to load the background images
            if isinstance(layer, pytmx.TiledImageLayer):
                l = layer.image
                offset = (layer.offsetx*self.scale, layer.offsety*self.scale) if hasattr(layer, 'offsetx') else (0, 0)
                print(offset)
                self.image.blit(pygame.transform.scale(l, (l.get_width()*self.scale, l.get_height()*self.scale)), offset)
            if isinstance(layer, pytmx.TiledTileLayer):
                tile = self.tiledData.get_tile_image_by_gid
                for x, y, gid, in layer:
                    tileImage = tile(gid)
                    if not tileImage is None:
                        tileImage = pygame.transform.scale(tileImage, (self.tiledData.tilewidth* self.scale, self.tiledData.tilewidth * self.scale))
                        self.image.blit(
                            tileImage, (x * self.tiledData.tilewidth * self.scale, y * self.tiledData.tileheight * self.scale))

        self.loadTiledObjects(start)
    
    def loadTiledObjects(self, start="Entrance"):
        for objT in self.tiledData.objects:
            #print(objT.name)
            objT.x, objT.y = objT.x * self.scale, objT.y * self.scale
            objT.width, objT.height = objT.width * self.scale, objT.height * self.scale
            try:  # This is the auto registering system that allows the level to detect the name and type of Tiled Objects and generates Sprites out of them.
                obj = objs.__dict__[objT.name]
                if objT.name == start: # This is basically how we are going to start the player on the map. It looks for an object type that matches the start key and then uses it to place the player
                        self.startSprite = obj(self.game, objT)  
                        self.sprites.add(self.startSprite)
                else:
                    self.sprites.add(obj(self.game, objT))
                
            except KeyError:
                try:
                    enemy = enemies.__dict__[objT.name]
                    self.sprites.add(enemy(self.game, objT))
                except KeyError:
                    print(f"Tiled Object {objT.name} is not defined")
    
    def getObjById(self, id):
        for obj in self.tiledData.objects:
            if obj.id == id:
                return obj
        return False
    
    def clearSprites(self):
        for s in self.sprites:
            s.kill()
