from xml.dom.pulldom import parseString
import pygame
import pytmx
from stgs import *
import enemies
import objects as objs
import os, json, re

class GameMap:
    def __init__(self, game, index=0):
        self.game = game
        self.floors = [
            Floor(game, "Floor1")
        ]
        self.index = index
        self.floor = self.floors[self.index]    # The floor loading will be based on an index within the floors list 

    def loadFloor(self, num=1):
        """Sets the map's floor and activates it"""
        self.floor = self.floors[num-1]
        self.floor.load()
    
    def switchRoom(self, room, startObj):
        for s in self.floor.room.sprites:
            s.kill()
            
        self.floor.enterRoom(room, startObj)
    
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
        for root, d, files in os.walk(self.folderPath):
            for f in files:
                self.roomPaths.append(os.path.join(root, f)) 
        
        print(self.roomPaths)
        # Generates room objects from path
        self.rooms = [Room(self, i) for i in self.roomPaths]
        # This stores the current room number or index within the rooms list 
        self.current = 0

    def load(self):
        """Loads the floor (by default in the first room)"""
        self.enterRoom("room1-floor1")

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
        self.scale = 1

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
                self.image.blit(pygame.transform.scale(l, (l.get_width()*self.scale, l.get_height()*self.scale)), (0, 0))
        
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
                elif objT.type == None:
                    self.sprites.add(obj(self.game, objT))
                else:
                    try:                                            # This code is quite complicated and slightly unecessary
                        for cl in obj.__subclasses__():             # What it does is just look to see if the object you are loading has a subclass
                            if cl.__name__ == objT.type:            # And then it sees if the subclass is the type of the tiled object 
                                obj = cl                            # And then creates an object based on that
                        self.sprites.add(obj(self.game, objT))
                    except KeyError:
                        print(
                            f"Tile Object {objT.name} with type {objT.type} is not defined")

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

# class Level:
#     def __init__(self, mapDir, **kwargs):
#         self.mapDir = mapDir
#         self.sprites = pygame.sprite.Group()
#         self.startSprite = None
#         self.scale = 3
#         self.width = winWidth
#         self.height = winHeight
#         self.levelSize = (self.width, self.height)
#         self.rect = pygame.Rect(0, 0, self.width, self.height)
#         self.loaded = False
#         self.name = os.path.splitext(os.path.basename(mapDir))[0]
        
#         for k, v in kwargs.items():
#             self.__dict__[k] = v

#     def load(self, game, start="entrance"):
#         #if not self.loaded:
#         self.game = game
#         self.clearSprites()
#         self.points = 0
#         self.loadTiled(start)
#         if self.startSprite:
#             self.game.player.setPos(self.startSprite.rect.center, True)
#         else:
#             self.game.player.setPos((self.width/2, self.height/2))

#     def loadTiled(self, start="entrance"):  # Map needs to be specified
#         self.enemyCnt = 0
#         self.tmxdata = pytmx.load_pygame(self.mapDir, pixelalpha=True)
#         print(self.tmxdata.layers)
#         self.width = self.tmxdata.width * self.tmxdata.tilewidth * self.scale
#         self.height = self.tmxdata.height * self.tmxdata.tileheight * self.scale
#         self.levelSize = (self.width, self.height)
#         self.rect = pygame.Rect(0, 0, self.width, self.height)
#         self.image = pygame.Surface(self.levelSize)

#         tile = self.tmxdata.get_tile_image_by_gid
#         for layer in self.tmxdata.visible_layers:
#             if isinstance(layer, pytmx.TiledTileLayer):
#                 # Load a tile layer
#                 for x, y, gid, in layer:
#                     tileImage = tile(gid)
#                     if not tileImage is None:
#                         tileImage = pygame.transform.scale(tileImage, (self.tmxdata.tilewidth* self.scale, self.tmxdata.tilewidth * self.scale))
#                         self.image.blit(
#                             tileImage, (x * self.tmxdata.tilewidth * self.scale, y * self.tmxdata.tileheight * self.scale))
#             if isinstance(layer, pytmx.TiledImageLayer):
#                 # Load an image layer
#                 pass
#                 # img = layer.image#pygame.image.load().image.convert_alpha()
#                 # print(vars(layer))
#                 # self.image.blit(pygame.transform.scale(img, (img.get_width()*self.scale, img.get_height()*self.scale)), (627, 1875))#(layer.offsetx* self.scale, layer.offsety* self.scale))

#         self.teleporters = pygame.sprite.Group()

#         for objT in self.tmxdata.objects:
#             #print(objT.name)
#             objT.x, objT.y = objT.x * self.scale, objT.y * self.scale
#             objT.width, objT.height = objT.width * self.scale, objT.height * self.scale
#             try:  # This is the auto registering system that allows the level to detect the name and type of Tiled Objects and generates Sprites out of them.
#                 obj = objs.__dict__[objT.name]
#                 if not objT.type == None:
#                     if objT.type == start: # This is basically how we are going to start the player on the map. It looks for an object type that matches the start key and then uses it to place the player
#                         self.startSprite = obj(self.game, objT)  
#                         self.sprites.add(self.startSprite)
#                     try:                                            # This code is quite complicated and slightly unecessary
#                         for cl in obj.__subclasses__():             # What it does is just look to see if the object you are loading has a subclass
#                             if cl.__name__ == objT.type:            # And then it sees if the subclass is the type of the tiled object 
#                                 obj = cl                            # And then creates an object based on that
#                         self.sprites.add(obj(self.game, objT))
#                     except KeyError:
#                         print(
#                             f"Tile Object {objT.name} with type {objT.type} is not defined")
#                 else:
#                     self.sprites.add(obj(self.game, objT))

#             except KeyError:
#                 try:
#                     enemy = enemies.Enemy
#                     if not objT.type == None:
#                         try:
#                             for cl in enemy.__subclasses__():
#                                 if cl.__name__ == objT.type:
#                                     enemy = cl
#                             self.sprites.add(enemy(self.game, objT))
#                         except KeyError:
#                             print(
#                                 f"Tiled Enemy Object {objT.type} is not defined")
#                     else:
#                         self.sprites.add(enemy(self.game, objT))
#                     self.enemyCnt += 1
#                 except KeyError:
#                     print(f"Tiled Object {objT.name} is not defined")

#             if objT.name == 'text':
#                 text = fonts['3'].render(
#                     objT.text, self.game.antialiasing, (255, 255, 255))
#                 self.image.blit(text, (objT.x, objT.y))
            
#         self.loaded = True

#     def getObjById(self, id):
#         for obj in self.tmxdata.objects:
#             if obj.id == id:
#                 return obj
#         return False
    
#     def clearSprites(self):
#         for s in self.sprites:
#             s.kill()

# Remember to include tileset image and tsx file with the tmx file of the map
#level1 = Level(asset('Tiled/cave1.tmx'))

# All Game levels
#gameLevels = [level1]
