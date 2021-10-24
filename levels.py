import pygame
import pytmx
from stgs import *
import enemies
import objects as objs
import os

class GameMap:
    def __init__(self, game):
        self.game = game
        self.levels = [
            Level(asset('Tiled/cave1.tmx')),
            Level(asset('Tiled/cave2.tmx'))
        ]
        self.level = self.levels[0]
    
    def switchLevel(self, name, start="entrance"):
        for l in self.levels:
            if l.name == name:
                self.loadLevel(l, start)
        
    def loadLevel(self, level=None, start="entrance"):
        self.level.clearSprites()
        self.level = level if level else self.level
        self.level.load(self.game, start)

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
        if not self.loaded:
            self.game = game
            for s in self.sprites:
                s.kill()
            self.points = 0
            self.loadTiled(start)
        if self.startSprite:
            self.game.player.setPos(self.startSprite.rect.center, True)
        else:
            self.game.player.setPos(self.width/2, self.height/2)

    def loadTiled(self, start="entrance"):  # Map needs to be specified
        self.enemyCnt = 0
        self.tmxdata = pytmx.load_pygame(self.mapDir, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth * self.scale
        self.height = self.tmxdata.height * self.tmxdata.tileheight * self.scale
        self.levelSize = (self.width, self.height)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.image = pygame.Surface(self.levelSize)

        tile = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tileImage = tile(gid)
                    if not tileImage is None:
                        tileImage = pygame.transform.scale(tileImage, (self.tmxdata.tilewidth* self.scale, self.tmxdata.tilewidth * self.scale))
                        self.image.blit(
                            tileImage, (x * self.tmxdata.tilewidth * self.scale, y * self.tmxdata.tileheight * self.scale))

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
level1 = Level(asset('Tiled/cave1.tmx'))

# All Game levels
gameLevels = [level1]
