import types
import json

import pygame
import pygame.locals
import shared


class Map() :


    def __init__(self,mapJsonPath) :

        self.groundImage = pygame.image.load("assets/ground.png")
        self.layers   = self.load(mapJsonPath)

    def render(self) :
    
        self.renderLayer("base")

    def load(self, mapJsonPath) :

        with open(mapJsonPath) as f :

            mapJson = json.load(f)

        self.layer  = {}
        self.width  = mapJson["width"]
        self.height = mapJson["height"]

        for layer in mapJson["layers"] :

            layerName = layer["name"]
            layerData_ = layer["data"]

            layerData = []
            for data in layerData_ :
                layerData.append(data-1)

            self.layer[layerName] = layerData

    def renderLayer(self, layerName) :

        layerToRender = self.layer[layerName]

        for (i, tileId) in enumerate(layerToRender) :

            xPix = (i % self.width) * shared.tileSize
            yPix = (i / self.width) * shared.tileSize

            if (tileId != -1) :
                shared.view.blit(shared.tileset.tiles[tileId], (xPix,yPix))

    def getWalkability(self, x_, y_) :

        if (x_ < 0) or (x_ >= self.width * shared.tileSize) \
        or (y_ < 0) or (y_ >= self.height * shared.tileSize) :
            return False
        
        neighbours = [ (1,1), (1,-1), (-1,1), (-1,-1) ]

        for dx, dy in neighbours :

            x = int(float(x_ + 0.5 * dx * shared.tileSize) / shared.tileSize)
            y = int(float(y_ + 0.5 * dy * shared.tileSize) / shared.tileSize)
            if (x < 0) or (x >= self.width) or (y < 0) or (y >= self.height) :
                return False

            i = x + y * self.width
            tileId = self.layer["base"][i]

            if (shared.tileset.mask[tileId] != 0) : return False
        
        return True





