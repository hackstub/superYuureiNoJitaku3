import pygame
import pygame.locals
import shared
from math import  sqrt

class Ennemy() :


    def __init__(self, pos) :

        self.x, self.y = pos
        self.loadSprites("assets/ennemy.png")
        self.orientation       = "front"
        self.currentSpriteStep = 0
        
        self.updateCurrentSprite()

    def loadSprites(self, path) :

        self.sprites          = {}
        self.sprites["front"] = []
        self.sprites["right"] = []
        self.sprites["left"]  = []
        self.sprites["back"]  = []
        spritesImage = pygame.image.load(path)
      
        self.sprites["front"].append(self.getSprite(spritesImage, 0, 0))
        self.sprites["front"].append(self.getSprite(spritesImage, 0, 1))
        self.sprites["left"] .append(self.getSprite(spritesImage, 1, 0))
        self.sprites["left"] .append(self.getSprite(spritesImage, 1, 1))
        self.sprites["back"] .append(self.getSprite(spritesImage, 2, 0))
        self.sprites["back"] .append(self.getSprite(spritesImage, 2, 1))
        self.sprites["right"].append(self.getSprite(spritesImage, 3, 0))
        self.sprites["right"].append(self.getSprite(spritesImage, 3, 1))
 
    def getSprite(self, spritesImage, x, y, s = 1) :

        return spritesImage.subsurface((x * shared.tileSize, 
                                        y * shared.tileSize,
                                        s * shared.tileSize, 
                                        s * shared.tileSize))

    def render(self) :
       
        spriteW = self.currentSprite.get_width()
        spriteH = self.currentSprite.get_height()
        
        shared.view.blit(self.currentSprite, (self.x - spriteW/2,  self.y-spriteH/2))


    def look(self, direction) :

        self.orientation = direction
        
        self.updateCurrentSprite()

    def move(self, direction) :
        
        self.look(direction)

        if   (self.orientation == "back" ) : dx, dy =  0, -2
        elif (self.orientation == "front") : dx, dy =  0, +2
        elif (self.orientation == "left" ) : dx, dy = -2, 0
        elif (self.orientation == "right") : dx, dy = +2, 0

        if (shared.map.getWalkability(self.x+dx, self.y+dy)) :
            self.x += dx
            self.y += dy

        self.x += dx
        self.y += dy


    def update(self) :
    
        Dx = shared.hero.x - self.x
        Dy = shared.hero.y - self.y

        r = sqrt(Dx*Dx+Dy*Dy)
        
        if (r >= shared.tileSize) :
            
            dx = 0.5 * Dx / r
            dy = 0.5 * Dy / r

            if (shared.map.getWalkability(self.x+dx, self.y+dy)) :
                self.x += dx
                self.y += dy


    def updateCurrentSprite(self) :

        self.currentSprite = self.sprites[self.orientation][self.currentSpriteStep]

    def gotHit(self) :

        heroX, heroY = shared.hero.x, shared.hero.y

        Dx = heroX - self.x
        Dy = heroY - self.y
        
        r = sqrt(Dx*Dx+Dy*Dy)
            
        dx = 10 * Dx / r
        dy = 10 * Dy / r
       
        self.x -= dx
        self.y -= dy

