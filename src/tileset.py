
import pygame
import pygame.locals
import shared

from PIL import Image


class Tileset() :


    def __init__(self, tilesetFolder) :

        self.loadTiles          (tilesetFolder+"/tiles.png")
        self.loadWalkabilityMask(tilesetFolder+"/walkability.png")
    
    def loadTiles(self, path) :

        tilesetImage = pygame.image.load(path)
        w, h = tilesetImage.get_size()
        
        self.tiles = []

        for tileY in range(0, h / shared.tileSize):
            for tileX in range(0, w / shared.tileSize):

                tile = (tileX * shared.tileSize, tileY * shared.tileSize, 
                                shared.tileSize,         shared.tileSize)
                
                self.tiles.append(tilesetImage.subsurface(tile))

    def loadWalkabilityMask(self, path) :

        maskImage = pygame.image.load(path)
        w, h = maskImage.get_size()

        self.walkabilityMask = [ ]

        for tileY in range(0, h / shared.tileSize):
            for tileX in range(0, w / shared.tileSize):

                tile = (tileX * shared.tileSize, tileY * shared.tileSize, 
                                shared.tileSize,         shared.tileSize)
                
                self.walkabilityMask.append(pygame.mask.from_surface(maskImage.subsurface(tile)))

