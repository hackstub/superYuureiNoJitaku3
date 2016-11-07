import pygame
import pygame.locals
import shared
from math import  sqrt

class Ennemy() :


    def __init__(self, pos) :

        self.x, self.y = pos
        self.loadSprites("assets/sprites/ennemy.png")
        self.orientation       = "front"
        self.currentSpriteStep = 0
        
        self.immunityCooldown = -1
        self.knockBack = None
        
        self.damageTexts = []

        self.alive = True
        self.hp = 200
        
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
        
        self.sprites["dead"] = self.getSprite(spritesImage, 4, 0)
 
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

        # Death management
       
        if (not self.alive) :
            self.deadCooldown -= 1
            self.updateCurrentSprite()

            if (self.deadCooldown <= 0) :
                self.destroy()
            return
        
        # Knockback

        if (self.knockBack != None) :
            self.updateKnockback()
            return

        # Standard IA

        Dx = shared.hero.x - self.x
        Dy = shared.hero.y - self.y

        r = sqrt(Dx*Dx+Dy*Dy)

        if (r >= shared.tileSize*0.7) :
        
            dx = shared.ennemyWalkingSpeed * Dx / r
            dy = shared.ennemyWalkingSpeed * Dy / r
            
            if (shared.isWalkable(self, (self.x+dx, self.y+dy))
            or (not shared.isWalkable(self, (self.x, self.y), ignoreEnnemies = True))) :
                self.x += dx
                self.y += dy


    def updateCurrentSprite(self) :

        if (self.alive) :
            self.currentSprite = self.sprites[self.orientation][self.currentSpriteStep]
        else :
            self.currentSprite = self.sprites["dead"].copy()
            self.currentSprite.fill((255,255,255,self.deadCooldown * 255 / 20), special_flags = pygame.BLEND_RGBA_MIN)


    def position(self) :
        return (self.x, self.y)

    def emmitDamage(self) :

        return [ shared.Damage(source=self, position=self.position(),
            radius=shared.tileSize*1.05, value=1) ]

    def mask(self) :

        return pygame.mask.from_surface(self.currentSprite)

    def destroy(self) :

        try : 
            shared.ennemies.remove(self)
            del self
        except :
            print "DELETING ENNEMY FAILED, LOL !"
     

    def receiveDamage(self, damage) :

        if not (self.alive) :
            return 
        
        if (self.immunityCooldown >= 0) :
            return
        
        damageSourceClass = damage.source.__class__.__name__

        if (damageSourceClass == self.__class__.__name__) :
            return

        self.hp -= damage.value
        if (self.hp <= 0) :
            self.alive = False
            self.deadCooldown = 20

        Dx = damage.source.x - self.x
        Dy = damage.source.y - self.y
        
        r = sqrt(Dx*Dx+Dy*Dy)

        dx = Dx / r
        dy = Dy / r

        knockBackForce = shared.ennemyKnockBack * damage.value/100
        if (knockBackForce < 3) : knockBackForce = 3

        self.damageTexts.append((damage.makeDamageText(),5))
        self.immunityCooldown = 10
        dx *= knockBackForce
        dy *= knockBackForce
        self.knockBack = (2, (dx, dy))
        self.updateKnockback()

    def updateKnockback(self) :

        cooldown, dp = self.knockBack
        dx, dy = dp

        if (shared.isWalkable(self, (self.x-dx, self.y-dy), ignoreEnnemies = True)) :
            self.x -= dx
            self.y -= dy
            cooldown -= 1
            self.knockBack = (cooldown, dp)
        
            if (cooldown < 0) : 
                if (shared.isWalkable(self, (self.x, self.y))) :
                    self.knockBack = None
        else : self.knockBack = None

    def dealtDamage(self, entity) :
        pass

