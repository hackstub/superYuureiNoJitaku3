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

        self.immunityCooldown = -1
        
        self.damageTexts = []

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
       
        shared.view.blit(self.currentSprite, (self.x, self.y))

        for damageText, cooldown in self.damageTexts :
            shared.view.blit(damageText, (self.x, self.y+cooldown-shared.tileSize/2))

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

        # Damage texts cooldown

        updatedDamageTexts = []
        for damageText, cooldown in self.damageTexts :
            cooldown -= 1
            if (cooldown < 0) : continue
            updatedDamageTexts.append((damageText,cooldown))
        self.damageTexts = updatedDamageTexts

        # Immunity cooldown

        if (self.immunityCooldown >= 0) :
            self.immunityCooldown -= 1

        # Movement

        Dx = shared.hero.x - self.x
        Dy = shared.hero.y - self.y

        r = sqrt(Dx*Dx+Dy*Dy)
        
        if (r >= shared.tileSize*0.7) :
            
            dx = shared.ennemyWalkingSpeed * Dx / r
            dy = shared.ennemyWalkingSpeed * Dy / r
            
            if (shared.isWalkable(self, (self.x+dx, self.y+dy))) :
                self.x += dx
                self.y += dy
                return
            #if not (shared.isWalkable(self, (self.x, self.y))) :
            #    self.x += dx
            #    self.y += dy
            #    return


    def updateCurrentSprite(self) :

        self.currentSprite = self.sprites[self.orientation][self.currentSpriteStep]

    def position(self) :
        return (self.x, self.y)

    def emmitDamage(self) :

        return [ shared.Damage(source=self, position=self.position(),
            radius=shared.tileSize*1.05, value=1) ]

    def receiveDamage(self, damage) :

        damageSourceClass = damage.source.__class__.__name__

        if (damageSourceClass == self.__class__.__name__) :
            return

        if (self.immunityCooldown >= 0) :
            return

        Dx = damage.source.x - self.x
        Dy = damage.source.y - self.y
        
        r = sqrt(Dx*Dx+Dy*Dy)

        Dx /= r
        Dy /= r
 
        
        knockBack = shared.ennemyKnockBack * damage.value/100
        if (knockBack < 3) : knockBack = 3

        self.knockBack(knockBack, (Dx, Dy))
        self.damageTexts.append((damage.makeDamageText(),5))
        self.immunityCooldown = 10

    def knockBack(self, knockBack, Dp) :

        Dx, Dy = Dp
        kOrigin = knockBack

        while knockBack > 0 :

            dx = knockBack * Dx
            dy = knockBack * Dy
          
            if (shared.isWalkable(self, (self.x-dx, self.y-dy), ignoreEnnemies = True)) :
                self.x -= dx
                self.y -= dy
                
                if not (shared.isWalkable(self, (self.x, self.y))) :
                    self.knockBack(kOrigin, Dp)
                return
            else :
                knockBack -= 1



