# from xml.dom.pulldom import parseString
import pygame
import pytmx
from stgs import *
import enemies
import objects as objs
import os

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
        for item in os.listdir(self.folderPath):
            f = os.path.join(self.folderPath, item)
            if os.path.isfile(f):
                self.roomPaths.append(f) 
        
        print(self.roomPaths)
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
        self.scale = 1

<<<<<<< HEAD
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
            if tobject.type != "Enemy":
                objc = objs.__dict__[tobject.type]
                obj = objc(self, tobject)
                self.objects.append(obj)
                if obj.objT.name == self.target and self.target:
                    twayEntrance = obj
            else:
                ec = enemies.__dict__[tobject.name]
                e = ec(self.floor.game, tobject)
                self.enemies.append(e)
        print(self.enemies)
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
        for enemy in self.enemies:
            if isinstance(enemy, (enemies.Rat)):
                pass
            self.image.blit(
                enemy.image,
                enemy.rect
            )
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
=======
        # Container for all the sprites corresponding to the room
>>>>>>> 0c63974b58c6c4bb2471f980809ad0380e6210df
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