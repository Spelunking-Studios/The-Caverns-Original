from xml.dom.pulldom import parseString
import pygame
import pytmx
from stgs import *
import enemies
import objects as objs
import os, json

class GameMap:
    def __init__(self, game):
        self.game = game
        self.floors = [
            Floor(game, 1)
        ]
        self.floor = self.floors[0]
    def update(self):
        """Update the map"""
        self.floor.update()
    def setFloor(self, num):
        """Sets the map's floor"""
        for f in self.levels:
            if f.floorNum == num:
                self.loadFloor(f)
    def loadFloor(self, floor=None):
        """Load the map's active floor"""
        self.floor.clear()
        self.floor = floor if floor else self.floor
        self.floor.load()

class Room:
    """Represents a single room"""
    def __init__(self, floor, roomFilePath, **kwargs):
        """Initialize the room"""
        self.floor = floor
        self.roomFilePath = roomFilePath
        self.scale = 3
        self.entranceNum = -1
        self.sprites = pygame.sprite.Group()
        self.width = winWidth * self.scale
        self.height = winHeight * self.scale
        self.rect = pygame.Rect((0, 0, self.width, self.height))
        self.loaded = False
        self.name = os.path.splitext(
            os.path.basename(self.roomFilePath)
        )[0]
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))
        self.bgImage = pygame.Surface((self.width, self.height))
        self.bgImage.fill((0, 255, 0))

        for k, v in kwargs.items():
            self.__dict__[k] = v
    def load(self):
        """Load the room's associated data"""
        self.loadTiledData()
    def loadTiledData(self):
        """Load data from the tiled file"""
        self.tiledData = pytmx.load_pygame(self.roomFilePath, pixelAlpha = True)
        for layer in self.tiledData.visible_layers:
            # Go through every layer till we reach the bg layer
            if isinstance(layer, pytmx.TiledImageLayer):
                # The background image layer
                self.bgImage = layer.image
        # Go through every object in the map
        entrances = [] # List of entrances
        twayEntrance = None # The entrance the player is exiting
        for tobject in self.tiledData.objects:
            print(tobject.type)
            if tobject.type == "Entrance":
                entrances.append(tobject)
        for entrance in entrances:
            if entrance.properties["entranceNumber"] == self.entranceNum:
                twayEntrance = entrance
        # Set the player's position to the entrance
        if twayEntrance:
            self.floor.game.player.setPos((twayEntrance.x, twayEntrance.y))
    def update(self):
        """Update the room"""
        self.image.blit(
            self.bgImage,
            self.bgImage.get_rect()
        )
    def enter(self, number):
        """Enter the room from an entrance"""
        self.entranceNum = number
        self.load()

class Floor:
    """Represents a floor"""
    def __init__(self, game, num):
        """Basic initialization of props"""
        self.game = game
        self.floorNum = num
        self.mappingsFilePath = asset(f"floorMappings/floor{self.floorNum}.json")
        self.rooms = []
        self.room = None
        self.loadMappings()
        self.initRooms()
    def load(self):
        """Load the floor"""
        self.enterRoom(0, 1)
    def update(self):
        """Update the floor"""
        self.room.update()
    def loadMappings(self):
        with open(self.mappingsFilePath, "r") as f:
            data = json.load(f)
            self.roomCount = data["numberOfRooms"]
    def initRooms(self):
        for i in range(1, self.roomCount + 1): # Add 1 to offset python's indexing starting at 0
            self.rooms.append(Room(
                self,
                asset(f"Tiled/room{i}-floor{self.floorNum}.tmx")
            ))
        self.room = self.rooms[0]
    def clear(self):
        pass
    def enterRoom(self, roomNumber, exitNumber):
        self.room = self.rooms[roomNumber]
        self.room.enter(exitNumber)

class Level:
    def __init__(self, mapDir, **kwargs):
        self.mapDir = mapDir
        self.sprites = pygame.sprite.Group()
        self.startSprite = None
        self.scale = 3
        self.width = winWidth
        self.height = winHeight
        self.levelSize = (self.width, self.height)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.loaded = False
        self.name = os.path.splitext(os.path.basename(mapDir))[0]
        
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def load(self, game, start="entrance"):
        #if not self.loaded:
        self.game = game
        self.clearSprites()
        self.points = 0
        self.loadTiled(start)
        if self.startSprite:
            self.game.player.setPos(self.startSprite.rect.center, True)
        else:
            self.game.player.setPos((self.width/2, self.height/2))

    def loadTiled(self, start="entrance"):  # Map needs to be specified
        self.enemyCnt = 0
        self.tmxdata = pytmx.load_pygame(self.mapDir, pixelalpha=True)
        print(self.tmxdata.layers)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth * self.scale
        self.height = self.tmxdata.height * self.tmxdata.tileheight * self.scale
        self.levelSize = (self.width, self.height)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.image = pygame.Surface(self.levelSize)

        tile = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # Load a tile layer
                for x, y, gid, in layer:
                    tileImage = tile(gid)
                    if not tileImage is None:
                        tileImage = pygame.transform.scale(tileImage, (self.tmxdata.tilewidth* self.scale, self.tmxdata.tilewidth * self.scale))
                        self.image.blit(
                            tileImage, (x * self.tmxdata.tilewidth * self.scale, y * self.tmxdata.tileheight * self.scale))
            if isinstance(layer, pytmx.TiledImageLayer):
                # Load an image layer
                pass
                # img = layer.image#pygame.image.load().image.convert_alpha()
                # print(vars(layer))
                # self.image.blit(pygame.transform.scale(img, (img.get_width()*self.scale, img.get_height()*self.scale)), (627, 1875))#(layer.offsetx* self.scale, layer.offsety* self.scale))

        self.teleporters = pygame.sprite.Group()

        for objT in self.tmxdata.objects:
            #print(objT.name)
            objT.x, objT.y = objT.x * self.scale, objT.y * self.scale
            objT.width, objT.height = objT.width * self.scale, objT.height * self.scale
            try:  # This is the auto registering system that allows the level to detect the name and type of Tiled Objects and generates Sprites out of them.
                obj = objs.__dict__[objT.name]
                if not objT.type == None:
                    if objT.type == start: # This is basically how we are going to start the player on the map. It looks for an object type that matches the start key and then uses it to place the player
                        self.startSprite = obj(self.game, objT)  
                        self.sprites.add(self.startSprite)
                    try:                                            # This code is quite complicated and slightly unecessary
                        for cl in obj.__subclasses__():             # What it does is just look to see if the object you are loading has a subclass
                            if cl.__name__ == objT.type:            # And then it sees if the subclass is the type of the tiled object 
                                obj = cl                            # And then creates an object based on that
                        self.sprites.add(obj(self.game, objT))
                    except KeyError:
                        print(
                            f"Tile Object {objT.name} with type {objT.type} is not defined")
                else:
                    self.sprites.add(obj(self.game, objT))

            except KeyError:
                try:
                    enemy = enemies.Enemy
                    if not objT.type == None:
                        try:
                            for cl in enemy.__subclasses__():
                                if cl.__name__ == objT.type:
                                    enemy = cl
                            self.sprites.add(enemy(self.game, objT))
                        except KeyError:
                            print(
                                f"Tiled Enemy Object {objT.type} is not defined")
                    else:
                        self.sprites.add(enemy(self.game, objT))
                    self.enemyCnt += 1
                except KeyError:
                    print(f"Tiled Object {objT.name} is not defined")

            if objT.name == 'text':
                text = fonts['3'].render(
                    objT.text, self.game.antialiasing, (255, 255, 255))
                self.image.blit(text, (objT.x, objT.y))
            
        self.loaded = True

    def getObjById(self, id):
        for obj in self.tmxdata.objects:
            if obj.id == id:
                return obj
        return False
    
    def clearSprites(self):
        for s in self.sprites:
            s.kill()

# Remember to include tileset image and tsx file with the tmx file of the map
#level1 = Level(asset('Tiled/cave1.tmx'))

# All Game levels
#gameLevels = [level1]
