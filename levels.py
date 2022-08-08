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
            Floor(self, game, 1)
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
    
    def update(self):
        """Update the map"""
        self.floor.update()

class Floor:
    """Represents a floor"""
    def __init__(self, map, game, num):
        """Basic initialization of props"""
        self.game = game
        self.map = map
        self.floorNum = num
        self.mappingsFilePath = asset(f"floorMappings/floor{self.floorNum}.json")
        self.rooms = []
        self.room = None
        self.loadMappings()
        self.initRooms()

    def load(self):
        """Load the floor"""
        # Enter the first room in the floor at the room's generic entrance
        self.enterRoom(0, None)

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
                i,
                asset(f"Tiled/Floor{self.floorNum}/room{i}.tmx")
            ))
        self.room = self.rooms[0]
        
    def clear(self):
        pass
    def enterRoom(self, roomNumber, target):
        self.room = self.rooms[roomNumber]
        self.room.enter(target)
    def changeRoom(self, target):
        # Get the room number from the target
        # Thanks for regex searching code
        # https://stackoverflow.com/a/15340694/15566643 - UltraInstinct
        if not isinstance(target, str):
            return
        roomNumber = int(re.search(
            "^[0-9]",
            re.split("^floor[0-9]-room", target)[1]
        ).group(0))
        print(f"Changing room to {roomNumber}...")
        self.enterRoom(roomNumber - 1, target)

class Room:
    """Represents a single room"""
    def __init__(self, floor, num, roomFilePath, **kwargs):
        """Initialize the room"""
        self.floor = floor
        self.roomFilePath = roomFilePath
        self.roomNum = num
        self.scale = 3
        self.entranceNum = -1
        self.objects = []
        self.width = winWidth * self.scale
        self.height = winHeight * self.scale
        self.rect = pygame.Rect((0, 0, self.width, self.height))
        self.loaded = False
        self.name = os.path.splitext(
            os.path.basename(self.roomFilePath)
        )[0]
        self.image = pygame.Surface((self.width, self.height))
        self.bgImage = pygame.Surface((self.width, self.height))
        self.target = None

        for k, v in kwargs.items():
            self.__dict__[k] = v
    def load(self):
        """Load the room's associated data"""
        self.objects = []
        self.loadTiledData()
        self.image.blit(
            self.bgImage,
            self.bgImage.get_rect()
        )
    def loadTiledData(self):
        """Load data from the tiled file"""
        self.tiledData = pytmx.load_pygame(self.roomFilePath, pixelAlpha = True)
        for layer in self.tiledData.visible_layers:
            # Go through every layer till we reach the bg layer
            if isinstance(layer, pytmx.TiledImageLayer):
                # The background image layer
                self.bgImage = layer.image
        twayEntrance = None # The entrance the player is exiting
        # Go through every object in the map
        for tobject in self.tiledData.objects:
            entrances = [] # List of entrances
            exits = [] # List of exits
            objc = objs.__dict__[tobject.type]
            obj = objc(self, tobject)
            self.objects.append(obj)
            if obj.objT.name == self.target and self.target:
                twayEntrance = obj
        # Set the player's position to the entrance
        if twayEntrance:
            tpos = (twayEntrance.rect.x, twayEntrance.rect.y)
            # Check to make sure the player doesn't land on the entrance/exit
            prect = self.getRealignedPlayerRect()
            center = [
                twayEntrance.rect.x + (twayEntrance.rect.width >> 2),
                twayEntrance.rect.y + (twayEntrance.rect.height >> 2)
            ]
            poses = [
                ( # Right
                    center[0] + twayEntrance.rect.width + prect.width,
                    center[1]
                ),
                ( # Left
                    center[0] - twayEntrance.rect.width - prect.width,
                    center[1]
                ),
                ( # Top
                    center[0],
                    center[1] - twayEntrance.rect.height - prect.height
                ),
                ( # Bottom
                    center[0],
                    center[1] + twayEntrance.rect.height + prect.height
                )
            ]
            opens = [
                True, # Right
                True, # Left
                True, # Top
                True # Bottom
            ]
            index = 0
            for pos in poses:
                if pos[0] < 0 or pos[1] < 0:
                    opens[index] = False
                    continue
                self.floor.game.player.setPos(pos)
                for o in self.objects:
                    if not isinstance(o, (objs.Exit, objs.Entrance)):
                        if o.rect.colliderect(self.floor.game.player.rect):
                            opens[index] = False
                            break
                index += 1
            del index
            index = 0
            for open in opens:
                if open:
                    self.floor.game.player.setPos(poses[index])
                    return
                index += 1
            del index
            self.floor.game.player.setPos(tpos, True)
    def getRealignedPlayerRect(self):
        c = list(self.floor.game.player.moveRect)
        c[0] += c[2] / 2
        c[1] += c[3] / 2
        return pygame.Rect(c)
    def update(self):
        """Update the room"""
        # Update the objects
        self.image.blit(
            self.bgImage,
            self.bgImage.get_rect()
        )
        prect = self.getRealignedPlayerRect()
        for obj in self.objects:
            if isinstance(obj, (objs.Exit, objs.Entrance)):
                pygame.draw.rect(
                    self.image,
                    (255, 255, 255),
                    obj.rect
                )
                # Check if the player is on the exit
                ppos = prect
                pygame.draw.circle(
                    self.image,
                    (0, 0, 255),
                    (ppos.x, ppos.y),
                    5
                )
                #sr = self.image.get_rect()
                #for x in range(sr.width):
                #    for y in range(sr.height):
                #        if obj.rect.collidepoint(x, y):
                #            self.image.set_at((x, y), (0, 0, 255))
                if obj.rect.collidepoint(ppos[0], ppos[1]):
                    if "target" in obj.objT.properties.keys():
                        t = obj.objT.properties["target"]
                    else:
                        t = None
                    self.exit(t)
    def enter(self, target):
        """Enter the room from an entrance
        
        If target is not None, the player will move to the specified target id
        """
        self.target = target
        if not self.target:
            self.target = f"floor{self.floor.floorNum}-room{self.roomNum}-entrance1"
        self.load()
    def exit(self, target):
        """Exit the romm from an exit
        
        If target is not None, the player will move to the specified target id
        """
        if not target:
            print("No target specified (is this intentional?)")
            return
        self.objects = []
        self.floor.changeRoom(target)

class Level:
    def __init__(self, mapDir, **kwargs):
        self.mapDir = mapDir
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

    def loadTiled(self, start="entrance"):  # Map needs to be specified
        self.enemyCnt = 0
        self.tmxdata = pytmx.load_pygame(self.mapDir, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth * self.scale
        self.height = self.tmxdata.height * self.tmxdata.tileheight * self.scale
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
