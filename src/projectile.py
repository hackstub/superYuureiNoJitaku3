import pygame
import pygame.locals
import shared

class Projectile() :


    def __init__(self, source, orientation, vect, timer) :

        self.x = source.x + vect[0]
        self.y = source.y + vect[1]

        self.source            = source
        self.orientation       = orientation
        self.vect              = vect
        self.timer             = timer
        self.currentSpriteStep = 0

        self.loadSprites("assets/sprites/arrow.png")
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
      
        shared.view.blit(self.currentSprite, (self.x, self.y))


    def look(self, direction) :

        self.orientation = direction
        
        self.updateCurrentSprite()

    def mask(self) :

        return pygame.mask.from_surface(self.currentSprite)

    def update(self) :
 
        if (not shared.isWalkable(self, self.position(), ignoreEnnemies = True, ignoreList = [ self.source ] )) :
            self.timer = -1

        if (self.timer < 0) :
            self.destroy()
            return

        self.x += self.vect[0]
        self.y += self.vect[1]
        
        self.timer -= 1


    def destroy(self) :

        try : 
            shared.projectiles.remove(self)
            del self
        except :
            print("DELETING PROJECTILE FAILED, LOL !")
                

    def updateCurrentSprite(self) :

        self.currentSprite = self.sprites[self.orientation][self.currentSpriteStep]

    def position(self) :
        return (self.x, self.y)

    def emmitDamage(self) :

        position = (self.x, self.y)

        return [ shared.Damage(source=self, position=position,
            radius=shared.tileSize*0.7, value=2) ]

    def receiveDamage(self, damage) :
        pass 
            
    def dealtDamage(self, entity) :
        self.timer = -1

