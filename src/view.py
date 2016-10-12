
import pygame
import pygame.locals
import shared

class View() : 


    def __init__(self, windowLabel, viewSize) :

        self.width, self.height = viewSize
        self.widthPix, self.heightPix = self.width * shared.tileSize, self.height * shared.tileSize 

        self.screen = pygame.display.set_mode( (self.widthPix, self.heightPix), 0, 32)
        pygame.display.set_caption(windowLabel)

        self.offset   = (0,0)

    def setCenter(self, position) :

        (center_x, center_y) = position
        offset_x = center_x - self.widthPix  / 2
        offset_y = center_y - self.heightPix / 2

        self.offset = (offset_x, offset_y)
    
    def reset(self) :

        self.screen.fill( (0,0,0) )

        offset_x = shared.hero.x - self.widthPix  / 2
        offset_y = shared.hero.y - self.heightPix / 2
        self.offset = (offset_x, offset_y)
 


    def blit(self, tile, position) :

        (pos_x    , pos_y   ) = position
        (offset_x , offset_y) = self.offset

        self.screen.blit(tile, (pos_x - offset_x, pos_y - offset_y))


    def drawCircle(self, color, position, radius, width) :

        x = int(position[0] - self.offset[0])
        y = int(position[1] - self.offset[1])
        pygame.draw.circle(self.screen, color, (x,y), int(radius), width)

