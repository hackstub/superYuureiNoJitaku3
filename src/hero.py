import pygame
import pygame.locals
import shared
from projectile import Projectile

class Hero() :


    def __init__(self, spritePath) :



        # Position hero on hero spawn

        for obj in shared.map.layer["objects"] :
            if (obj == -1) : continue
            if (obj.__class__.__name__ != "SpawnHero") : continue
            self.x = obj.x
            self.y = obj.y
            break

        self.loadSprites(spritePath)
       
        self.orientation       = "front"
        self.currentSpriteStep = 0
        self.currentSpriteStepTempo = shared.heroWalkingSpriteTempo
        self.busy = False
        
        self.immunityCooldown = -1
        self.rangedAttackCooldown = -1

        self.updateCurrentSprite()
        
    def position(self) :

        return (self.x, self.y)

    def loadSprites(self, path) :

        self.sprites          = {}
        self.sprites["front"] = []
        self.sprites["right"] = []
        self.sprites["left"]  = []
        self.sprites["back"]  = []
        self.sprites["attack-front"] = []
        self.sprites["attack-right"] = []
        self.sprites["attack-left"]  = []
        self.sprites["attack-back"]  = []
        
        spritesImage = pygame.image.load(path)
      
        self.sprites["front"].append(self.getSprite(spritesImage, 0, 0))
        self.sprites["front"].append(self.getSprite(spritesImage, 0, 1))
        self.sprites["left"] .append(self.getSprite(spritesImage, 1, 0))
        self.sprites["left"] .append(self.getSprite(spritesImage, 1, 1))
        self.sprites["back"] .append(self.getSprite(spritesImage, 2, 0))
        self.sprites["back"] .append(self.getSprite(spritesImage, 2, 1))
        self.sprites["right"].append(self.getSprite(spritesImage, 3, 0))
        self.sprites["right"].append(self.getSprite(spritesImage, 3, 1))
 
        self.sprites["attack-front"].append(self.getSprite(spritesImage, 4,  0, 3))
        self.sprites["attack-front"].append(self.getSprite(spritesImage, 4,  3, 3))
        self.sprites["attack-front"].append(self.getSprite(spritesImage, 4,  6, 3))
        self.sprites["attack-left"] .append(self.getSprite(spritesImage, 7,  0, 3))
        self.sprites["attack-left"] .append(self.getSprite(spritesImage, 7,  3, 3))
        self.sprites["attack-left"] .append(self.getSprite(spritesImage, 7,  6, 3))
        self.sprites["attack-back"] .append(self.getSprite(spritesImage, 10, 0, 3))
        self.sprites["attack-back"] .append(self.getSprite(spritesImage, 10, 3, 3))
        self.sprites["attack-back"] .append(self.getSprite(spritesImage, 10, 6, 3))
        self.sprites["attack-right"].append(self.getSprite(spritesImage, 13, 0, 3))
        self.sprites["attack-right"].append(self.getSprite(spritesImage, 13, 3, 3))
        self.sprites["attack-right"].append(self.getSprite(spritesImage, 13, 6, 3))



    def getSprite(self, spritesImage, x, y, s = 1) :
        return spritesImage.subsurface((x * shared.tileSize, y * shared.tileSize,
                                        s * shared.tileSize, s * shared.tileSize))


    def render(self) :
        
        shared.view.blit(self.currentSprite, (self.x, self.y))


    def look(self, direction) :

        if (self.busy) : 
            return

        self.orientation = direction
        
        self.updateCurrentSprite()

    def move(self, direction) :
        
        if (self.busy) :
            return

        self.look(direction)

        dx, dy = shared.directionToVector(self.orientation, shared.heroWalkingSpeed)

        if (shared.isWalkable(self, (self.x+dx, self.y+dy))) :
            self.x += dx
            self.y += dy

        self.spriteUpdate()


    def mask(self) :

        return pygame.mask.from_surface(self.currentSprite)

    def meleeAttackKeyHandler(self) :

        if (self.busy) :
            return

        self.busy = "attack"
        self.currentSpriteStepTempo = shared.heroAttackSpriteTempo
        self.updateCurrentSprite()
        
    def rangedAttackKeyHandler(self) :

        if (self.busy) :
            return

        if (self.rangedAttackCooldown >= 0) :
            return

        vect = shared.directionToVector(self.orientation, shared.tileSize / 2)
        shared.projectiles.add(Projectile(self, self.orientation, vect, timer=10))

        self.rangedAttackCooldown = 10

    def emmitDamage(self) :


        if (self.busy != "attack") :
            return [ ]

        if   (self.orientation == "back" ) : hittedNeighbour = [ (1, 0), (0.7,-0.7),  ( 0,-1) ][self.currentSpriteStep]
        elif (self.orientation == "front") : hittedNeighbour = [ (-1,0), (-0.7, 0.7), ( 0, 1) ][self.currentSpriteStep]
        elif (self.orientation == "left" ) : hittedNeighbour = [ (0,-1), (-0.7,-0.7), (-1, 0) ][self.currentSpriteStep]
        elif (self.orientation == "right") : hittedNeighbour = [ (0,-1), ( 0.7,-0.7), ( 1, 0) ][self.currentSpriteStep]
        
        hittedPosition = (self.x + hittedNeighbour[0]*shared.tileSize, 
                          self.y + hittedNeighbour[1]*shared.tileSize)

        return [ shared.Damage(source=self, position=hittedPosition,
            radius=shared.tileSize*0.7, value=123) ]



    def receiveDamage(self, damage) :
        
        if (self.immunityCooldown >= 0) :
            return

        print("Hero took "+str(damage.value)+" damages !")
        self.immunityCooldown = 10




    def update(self) :
   
        if (self.immunityCooldown >= 0) :
            self.immunityCooldown -= 1
        
        if (self.rangedAttackCooldown >= 0) :
            self.rangedAttackCooldown -= 1

        if (self.busy) :
            self.spriteUpdate()
     
    def spriteUpdate(self) :
        
        self.currentSpriteStepTempo -= 1
        
        if (self.currentSpriteStepTempo >= 0) :
            return
        
        self.currentSpriteStep += 1

        if not (self.busy) :
            self.currentSpriteStepTempo = shared.heroWalkingSpriteTempo
            spriteName = self.orientation
        else :
            self.currentSpriteStepTempo = shared.heroAttackSpriteTempo
            spriteName = self.busy+"-"+self.orientation
        
        if (self.currentSpriteStep >= len(self.sprites[spriteName])) :
            self.currentSpriteStep = 0
        
        if (self.busy) and (self.currentSpriteStep == 0) :
            self.busy = False
        
        self.updateCurrentSprite()

    def updateCurrentSprite(self) :

        if not (self.busy) :
            spriteName = self.orientation
        else :
            spriteName = self.busy+"-"+self.orientation
        
        self.currentSprite = self.sprites[spriteName][self.currentSpriteStep]

    def dealtDamage(self, entity) :
        pass

