
import pygame
import pygame.locals
import shared
from PIL import Image, ImageFilter

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

        self.screen.fill( (255,0,255) )

        offset_x = shared.hero.x - self.widthPix  / 2
        offset_y = shared.hero.y - self.heightPix / 2
        self.offset = (offset_x, offset_y)
 


    def blit(self, tile, position, debug = False) :

        (x,        y       ) = position
        (offset_x, offset_y) = self.offset

        w, h = tile.get_size()

        if (debug) :
            s = pygame.Surface((100,100), pygame.SRCALPHA)
            s.fill((255,255,255,200)) 
            tile = tile.copy()
            tile.blit(s,(0,0))

        self.screen.blit(tile, (x - w/2 - offset_x, y - h/2 - offset_y))



    def drawCircle(self, color, position, radius, width) :

        x = int(position[0] - self.offset[0])
        y = int(position[1] - self.offset[1])
        pygame.draw.circle(self.screen, color, (x,y), int(radius), width)




    def makeMaskFromPolygon(self, vertices, blurRadius = 3) :
        
        initsize = 2000
        margin = 25
        
        # Base surface filled with black
        base = pygame.Surface((initsize,initsize), flags=pygame.SRCALPHA)
        base.fill((0,0,0,0))

        # Draw polygon in center of base, with white color
        offseted_vertices = [ (x+initsize/2,y+initsize/2) for x,y in vertices ]
        rect = pygame.draw.polygon(base, (255,255,255,255), offseted_vertices)
      
        # Extract only the polygon part
        surf = base.subsurface((rect.x     -   margin, rect.y      -   margin,
                                rect.width + 2*margin, rect.height + 2*margin))
        
        offset_x = initsize/2-rect.x+margin
        offset_y = initsize/2-rect.y+margin
        

        # Convert the surface to PIL image
        surf_size = surf.get_size()
        surf_in_string = pygame.image.tostring(surf, "RGBA", False)
        pil_image = Image.frombytes("RGBA",surf_size, surf_in_string)

        # Blur image using PIL
        pil_blured = pil_image.filter(ImageFilter.GaussianBlur(radius=blurRadius))

        # Convert it back to a pygame surface
        surf = pygame.image.fromstring(pil_blured.tobytes("raw", "RGBA"), surf_size, "RGBA")

        return (offset_x, offset_y, surf)


    def setGlobalMask(self, size, maskList) :

        globalW, globalH = size
        self.globalMask = pygame.Surface((globalW, globalH), flags=pygame.SRCALPHA)
        self.globalMask.fill((0,0,0,255))
       

        for mask in maskList :
        
            print maskList
            
            x, y = mask["x"], mask["y"]
            surf = mask["surf"]
            w, h = surf.get_size() 
            
            for i in range(0,w) :
                for j in range(0,h) :
                    m = surf.get_at((i,j))
                    b = self.globalMask.get_at((x+i,y+j))
                    a = b[3] - m[0]
                    if (a < 0) : a = 0
                    b = self.globalMask.set_at((x+i,y+j), (b[0], b[1], b[2], a))

    def renderGlobalMask(self) :

        (offset_x, offset_y) = self.offset
        self.screen.blit(self.globalMask, (- offset_x, -offset_y))












