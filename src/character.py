import pygame
import pygame.locals
import shared

class Character() :


    def __init__(self, spritePath) :

        self.x = shared.map.width  * shared.tileSize / 2 
        self.y = shared.map.height * shared.tileSize / 2 
       
        self.loadSprites(spritePath)
       
        self.orientation       = "front"
        self.currentSpriteStep = 0
        self.currentSpriteStepTempo = 2
        self.busy = False
        
        self.updateCurrentSprite()
        

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
        self.sprites["attack-left"] .append(self.getSprite(spritesImage, 7, 0, 3))
        self.sprites["attack-left"] .append(self.getSprite(spritesImage, 7, 3, 3))
        self.sprites["attack-left"] .append(self.getSprite(spritesImage, 7, 6, 3))
        self.sprites["attack-back"] .append(self.getSprite(spritesImage, 10,  0, 3))
        self.sprites["attack-back"] .append(self.getSprite(spritesImage, 10,  3, 3))
        self.sprites["attack-back"] .append(self.getSprite(spritesImage, 10,  6, 3))
        self.sprites["attack-right"].append(self.getSprite(spritesImage, 13, 0, 3))
        self.sprites["attack-right"].append(self.getSprite(spritesImage, 13, 3, 3))
        self.sprites["attack-right"].append(self.getSprite(spritesImage, 13, 6, 3))



    def getSprite(self, spritesImage, x, y, s = 1) :
        return spritesImage.subsurface((x * shared.tileSize, y * shared.tileSize,
                                        s * shared.tileSize, s * shared.tileSize))


    def render(self) :
       
        spriteW = self.currentSprite.get_width()
        spriteH = self.currentSprite.get_height()
        
        shared.view.blit(self.currentSprite, (self.x - spriteW/2,  self.y-spriteH/2))


    def look(self, direction) :

        if (self.busy) : 
            return

        self.orientation = direction
        
        self.updateCurrentSprite()

    def move(self, direction) :
        
        if (self.busy) :
            return

        self.look(direction)

        if   (self.orientation == "back" ) : dx, dy =  0, -2
        elif (self.orientation == "front") : dx, dy =  0, +2
        elif (self.orientation == "left" ) : dx, dy = -2, 0
        elif (self.orientation == "right") : dx, dy = +2, 0
        
        if (shared.map.getWalkability(self.x+dx, self.y+dy)) :
            self.x += dx
            self.y += dy

        self.spriteUpdate()

    def attackKeyHandler(self) :

        if (self.busy) :
            return

        self.busy = "attack"
        self.currentSpriteStepTempo = 2
        self.updateCurrentSprite()
        
        if   (self.orientation == "back" ) : hittedNeighbours = [ (0,-1),( 0.7,-0.7), ( 1,0) ] 
        elif (self.orientation == "front") : hittedNeighbours = [ (0, 1),(-0.7, 0.7), (-1,0) ] 
        elif (self.orientation == "left" ) : hittedNeighbours = [ (0,-1),(-0.7,-0.7), (-1,0) ] 
        elif (self.orientation == "right") : hittedNeighbours = [ (0,-1),( 0.7,-0.7), ( 1,0) ] 
    
        hittedPositions = []
        for nX, nY in hittedNeighbours :
            hittedPositions.append((self.x + nX * shared.tileSize, 
                                    self.y + nY * shared.tileSize))



        shared.ennemyManager.propagateAttackFromHero(hittedPositions)


    def update(self) :
    
        if (self.busy) :
            self.spriteUpdate()
     
    def spriteUpdate(self) :
        
        self.currentSpriteStepTempo -= 1
        
        if (self.currentSpriteStepTempo >= 0) :
            return
        
        self.currentSpriteStepTempo = 2
        self.currentSpriteStep += 1

        if not (self.busy) :
            spriteName = self.orientation
        else :
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

