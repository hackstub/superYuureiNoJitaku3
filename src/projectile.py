import pygame
import pygame.locals
import shared

class Projectile() :


    def __init__(self, source, orientation, vect, timer) :

        self.x = source.x + vect[0]
        self.y = source.y + vect[1]

        self.orientation       = orientation
        self.vect              = vect
        self.timer             = timer
        self.currentSpriteStep = 0

        self.loadSprites("assets/arrow.png")
        self.updateCurrentSprite()

    def loadSprites(self, path) :

        self.sprites          = {}
        self.sprites["front"] = []
        self.sprites["right"] = []
        self.sprites["left"]  = []
        self.sprites["back"]  = []

        spritesImage = pygame.image.load(path)
      
        self.sprites["front"].append(self.getSprite(spritesImage, 0, 0))
        self.sprites["left"] .append(self.getSprite(spritesImage, 1, 0))
        self.sprites["back"] .append(self.getSprite(spritesImage, 2, 0))
        self.sprites["right"].append(self.getSprite(spritesImage, 3, 0))
 
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


    def update(self) :
    
        self.x += self.vect[0]
        self.y += self.vect[1]
        
        self.timer -= 1

        if (self.timer < 0) :
            shared.projectiles.remove(self)
            del self

    def updateCurrentSprite(self) :

        self.currentSprite = self.sprites[self.orientation][self.currentSpriteStep]

    def position(self) :
        return (self.x, self.y)

    def emmitDamage(self) :

        position = (self.x+2*self.vect[0], self.y+2*self.vect[1])

        return [ shared.Damage(source=self, position=position,
            radius=shared.tileSize*0.7, value=1) ]

    def receiveDamage(self, damage) :

        self.timer = -1
            


