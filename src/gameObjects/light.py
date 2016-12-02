import shared
import pygame
from gameObjects.gameObject import GameObject
import random

class Light(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo, properties)

        self.loadSprites()

        self.nextSpriteCooldown = -1
        self.currentSpriteId = random.randint(1,3)

        self.update()
   
    def loadSprites(self) :

        self.sprites = [ ]
        spritesImage = pygame.image.load("./assets/sprites/light.png")
      
        for i in range(12) :
            self.sprites.append(self.getSprite(spritesImage, i, 0))

        self.halos = [ ]
        halosImage = pygame.image.load("./assets/sprites/halo.png")
      
        for i in range(4) :
            self.halos.append(self.getSprite(halosImage, i*3, 0, 3))


    def getSprite(self, spritesImage, x, y, s = 1) :

        return spritesImage.subsurface((x * shared.tileSize, 
                                        y * shared.tileSize,
                                        s * shared.tileSize, 
                                        s * shared.tileSize))

    def update(self) :
        
        self.nextSpriteCooldown -= 1

        if (self.nextSpriteCooldown < 0) :
            self.nextSpriteCooldown = 6 + random.randint(1,3)
            self.currentSpriteId += 1
            if (self.currentSpriteId >= len(self.sprites)) :
                self.currentSpriteId = 0

            self.tile = self.sprites[self.currentSpriteId]
            self.halo = self.halos[self.currentSpriteId%4]

        return False
            
    def render(self) :

        if (self.active) and (self.visible) :
            shared.view.blit(self.halo, (self.x, self.y))
            shared.view.blit(self.tile, (self.x, self.y))







