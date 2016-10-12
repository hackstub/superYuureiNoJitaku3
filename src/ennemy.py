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

    #def move(self, direction) :
    #    
    #    self.look(direction)
    #
    #    if   (self.orientation == "back" ) : dx, dy =  0, -shared.ennemyWalkingSpeed
    #    elif (self.orientation == "front") : dx, dy =  0, +shared.ennemyWalkingSpeed
    #    elif (self.orientation == "left" ) : dx, dy = -shared.ennemyWalkingSpeed, 0
    #    elif (self.orientation == "right") : dx, dy = +shared.ennemyWalkingSpeed, 0
    #
    #    if (shared.map.getWalkability(self.x+dx, self.y+dy)) :
    #        self.x += dx
    #        self.y += dy
    #
    #    self.x += dx
    #    self.y += dy


    def update(self) :
    
        Dx = shared.hero.x - self.x
        Dy = shared.hero.y - self.y

        r = sqrt(Dx*Dx+Dy*Dy)
        
        if (r >= shared.tileSize) :
            
            dx = shared.ennemyWalkingSpeed * Dx / r
            dy = shared.ennemyWalkingSpeed * Dy / r

            if (shared.map.getWalkability(self.x+dx, self.y+dy)) :
                self.x += dx
                self.y += dy


    def updateCurrentSprite(self) :

        self.currentSprite = self.sprites[self.orientation][self.currentSpriteStep]

    def position(self) :
        return (self.x, self.y)

    def emmitDamage(self) :

        return [ shared.Damage(source=self, position=self.position(), radius=shared.tileSize, value=1) ]

    def receiveDamage(self, damage) :

        Dx = damage.source.x - self.x
        Dy = damage.source.y - self.y
        
        r = sqrt(Dx*Dx+Dy*Dy)
            
        dx = shared.ennemyKnockBack * Dx / r
        dy = shared.ennemyKnockBack * Dy / r
       
        self.x -= dx
        self.y -= dy

