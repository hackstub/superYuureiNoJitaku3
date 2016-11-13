import types
import json

import pygame
import pygame.locals
import shared


class Map() :


    def __init__(self,mapJsonPath) :

        self.load(mapJsonPath)
        self.makeWalkabilityMask()


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
            elif (layerName == "vision") :
                self.makeVisionLayer(layer["objects"])

            self.layer[layerName] = layerData
        
    def pixelSize(self) :
        return (self.width * shared.tileSize, self.height * shared.tileSize)

    def makeObjectLayer(self, data) :

        objectLayer = []

        for i in range(0,self.width * self.height) :
            objectLayer.append(-1)

        for obj in data :

            x = int(int(obj["x"]) / int(obj["width"]))
            y = int(int(obj["y"]) / int(obj["width"])) - 1

            tileId     = obj["gid"]
            objType    = obj["type"]
            properties = obj.get("properties",None)
            name       = obj["name"]

            #print "Loading object " + name + " (" + objType + ") ..."

            c = shared.strToObjectClass(objType)
            theObj = c(name, x, y, (tileId, shared.tileset.tiles[tileId - 1]), properties)
            objectLayer[x + y * self.width] = theObj

        return objectLayer

    def makeVisionLayer(self, data) :
       
        for obj in data :

            if (obj["type"] != "FieldOfVision") : continue
           
            #print "Loading field of vision for "+obj["name"]
            shared.visionManager.addZone(obj)
            
    def renderLayer(self, layerName) :

        layerToRender = self.layer[layerName]

        for (i, tile) in enumerate(layerToRender) :
            
            if (tile == -1) : continue

            xPix = (int(i % self.width) + 0.5) * shared.tileSize
            yPix = (int(i / self.width) + 0.5) * shared.tileSize

            if (type(tile) == int) :
                shared.view.blit(shared.tileset.tiles[tile], (xPix,yPix))
            else :
                tile.render()

    def update(self) :
    
        for obj in self.layer["objects"] :
           if (type(obj) != int) : obj.update()

    def render(self) :
    
        self.renderLayer("ground")
        self.renderLayer("mid")
        self.renderLayer("objects")

    def makeWalkabilityMask(self) :

        mask = pygame.mask.Mask(self.pixelSize())

        for layerName in [ "ground", "mid"] :
            for (i, tile) in enumerate(self.layer[layerName]) :
                
                if (tile == -1) : continue

                xPix = int((i % self.width) + 0.5) * shared.tileSize
                yPix = int((i / self.width) + 0.5) * shared.tileSize

                mask.draw(shared.tileset.walkabilityMask[tile], (xPix,yPix))

        self.walkabilityMask = mask

    def isWalkable(self, mask, pos) :

        x_, y_ = pos
        x_ = int(round(x_))
        y_ = int(round(y_))
        
        if (x_ < 0) or (x_ >= self.width * shared.tileSize) \
        or (y_ < 0) or (y_ >= self.height * shared.tileSize) :
            return False
        
        mask_w, mask_h = mask.get_size()
        offset = (x_ - int(mask_w/2), y_ - int(mask_h/2))

        if (self.walkabilityMask.overlap(mask, offset)) :
            return False
        else : 
            return True
      






