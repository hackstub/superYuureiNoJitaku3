import types
import json

import pygame
import pygame.locals
import shared


class Map() :


    def __init__(self,mapJsonPath) :

        self.layers   = self.load(mapJsonPath)


    def load(self, mapJsonPath) :

        with open(mapJsonPath) as f :

            mapJson = json.load(f)

        self.layer  = {}
        self.width  = mapJson["width"]
        self.height = mapJson["height"]

        for layer in mapJson["layers"] :

            layerName = layer["name"]
            
            if (layer["type"] == "tilelayer") :
                layerData = [ data-1 for data in layer["data"] ]
            elif (layerName == "objects") :
                layerData = self.makeObjectLayer(layer["objects"])
            else :
                print "SKIPPING UNKNOWN LAYER"+layerName+" LOL !"

            self.layer[layerName] = layerData

    def makeObjectLayer(self, data) :

        objectLayer = []

        for i in range(0,self.width * self.height) :
            objectLayer.append(None)

        for obj in data :

            print obj["type"]
            print obj["name"]

            x = int(obj["x"]) / int(obj["width"])
            y = int(obj["y"]) / int(obj["width"]) - 1

            tileId     = obj["gid"]
            objType    = obj["type"]
            properties = obj.get("properties",None)
            name       = obj["name"]

            #c = shared.strToObjectClass(objType)
            print "Attempting to load a " + objType + " objects"
            print name
            print x, y
            print properties
            #theObj = c(name, x, y, (tileId, self.tileset.tiles[tileId - 1]), properties)
            #objectLayer[x + y * self.width] = theObj

        return objectLayer

    def renderLayer(self, layerName) :

        layerToRender = self.layer[layerName]

        #print layerToRender

        for (i, tileId) in enumerate(layerToRender) :

            xPix = ((i % self.width) + 0.5) * shared.tileSize
            yPix = ((i / self.width) + 0.5) * shared.tileSize

            if (tileId != -1) :
                shared.view.blit(shared.tileset.tiles[tileId], (xPix,yPix))

    def update(self) :

        pass        

    def render(self) :
    
        self.renderLayer("ground")
        self.renderLayer("mid")
        #self.renderLayer("objects")

    def isWalkable(self, pos) :

        x_, y_ = pos

        if (x_ < 0) or (x_ >= self.width * shared.tileSize) \
        or (y_ < 0) or (y_ >= self.height * shared.tileSize) :
            return False
       
        neighbours = [ (1,1), (1,-1), (-1,1), (-1,-1) ]

        for dx, dy in neighbours :

            x = int(float(x_ + 0.3 * dx * shared.tileSize) / shared.tileSize)
            y = int(float(y_ + 0.3 * dy * shared.tileSize) / shared.tileSize)
            if (x < 0) or (x >= self.width) or (y < 0) or (y >= self.height) :
                return False

            i = x + y * self.width
            tileIdGround = self.layer["ground"][i]
            tileIdMid    = self.layer["mid"][i]

            if (shared.tileset.mask[tileIdGround] != 0) : return False
            if (shared.tileset.mask[tileIdMid]    != 0) : return False
        
        return True





