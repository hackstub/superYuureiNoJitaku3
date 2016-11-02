import shared
import pygame
import pygame.locals

from PIL import Image, ImageFilter


class VisionManager() :


    def __init__(self) :

        self.zones = {}
        self.activeZones = []
    
        self.globalMask = None

    def addZone(self, zone) :

        vertices = [ (pos["x"], pos["y"]) for pos in zone["polyline"] ]
        
        offset_x, offset_y, mask = self.makeZoneMask(vertices)
        corner_x, corner_y = zone["x"] - offset_x, zone["y"] - offset_y

        self.zones[zone["name"]] = { "corner"   : (corner_x, corner_y),
                                     "mask"     : mask }
    
    def makeZoneMask(self, vertices) :
        
        blurRadius = 20
        initsize = 2000
        margin = 150

        # Base surface filled with black
        base = pygame.Surface((initsize,initsize), flags=pygame.SRCALPHA)

 
        if (shared.debug) :
            base.fill((30,30,30,230))
        else :
            base.fill((30,30,30,255))

        # Draw polygon in center of base, with white color
        offseted_vertices = [ (x+initsize/2,y+initsize/2) for x,y in vertices ]
        #rect = pygame.draw.polygon(base, (255,255,255,0), offseted_vertices)
        rect = pygame.draw.polygon(base, (255,255,255,0), offseted_vertices)
      
        # Extract only the polygon part
        surf = base.subsurface((rect.x     -     margin , rect.y      -     margin,
                                rect.width + 2 * margin , rect.height + 2 * margin))
        
        offset_x = initsize/2-rect.x + margin
        offset_y = initsize/2-rect.y + margin

        # Convert the surface to PIL image
        surfSize = surf.get_size()
        surfInString = pygame.image.tostring(surf, "RGBA", False)
        surfPIL = Image.frombytes("RGBA", surfSize, surfInString)

        # Blur image using PIL
        surfPILblurred = surfPIL.filter(ImageFilter.GaussianBlur(radius=blurRadius))

        # Convert it back to a pygame surface
        surf = pygame.image.fromstring(surfPILblurred.tobytes("raw", "RGBA"), surfSize, "RGBA")

        return (offset_x, offset_y, surf)
        
    def heroInZone(self, zone) :
 
        heroX, heroY = shared.hero.position()

        heroX = int(heroX)
        heroY = int(heroY)

        w, h = zone["mask"].get_size()
        cornerX, cornerY = zone["corner"]
        xOnSurf = heroX - cornerX
        yOnSurf = heroY - cornerY

        if (xOnSurf < 0) or (yOnSurf < 0) or (xOnSurf > w) or (yOnSurf > h) :
            return False

        pix = zone["mask"].get_at((xOnSurf, yOnSurf))

        if (pix[0] > 127) :
            return True

        return False

    def update(self) :

        previousActiveZones = list(self.activeZones)

        for zoneName, zone in self.zones.items() :
        
            inZone = self.heroInZone(zone)
            if (inZone) and (zoneName not in self.activeZones) :
                self.activeZones.append(zoneName)
            elif (not inZone) and (zoneName in self.activeZones) :
                self.activeZones.remove(zoneName)

        if (previousActiveZones != self.activeZones) :
            self.remakeMask()

    def render(self) :

        if (self.globalMask != None) :
            shared.view.blitRaw(self.globalMask, (0,0))

    def remakeMask(self) :
        
        # Prepare base surface

        globalW, globalH = shared.map.pixelSize()
        globalMask = pygame.Surface((globalW, globalH), flags=pygame.SRCALPHA)
        
        if (shared.debug) :
            globalMask.fill((30,30,30,230))
        else :
            globalMask.fill((30,30,30,255))

        # Draw all the active zone

        for zoneName in self.activeZones :

            x, y = self.zones[zoneName]["corner"]
            w, h = self.zones[zoneName]["mask"].get_size()

            globalMask.blit(self.zones[zoneName]["mask"], (x,y), special_flags=pygame.BLEND_RGBA_MIN)


        self.globalMask = globalMask

        return





