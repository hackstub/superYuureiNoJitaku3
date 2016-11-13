import shared
import pygame
import pygame.locals

from PIL import Image, ImageFilter


class VisionManager() :


    def __init__(self) :

        self.zones = {}
        self.activeZones = []
    
        self.globalOverlay = None

    def addZone(self, zone) :

        vertices = [ (pos["x"], pos["y"]) for pos in zone["polyline"] ]
        
        offset_x, offset_y, overlay = self.makeZoneOverlay(vertices)
        corner_x, corner_y = zone["x"] - offset_x, zone["y"] - offset_y

        self.zones[zone["name"]] = { "corner"   : (corner_x, corner_y),
                                     "overlay"  : overlay }
    
    def makeZoneOverlay(self, vertices) :
        
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
        
        offset_x = int(initsize/2)-rect.x + margin
        offset_y = int(initsize/2)-rect.y + margin

        # Convert the surface to PIL image
        surfSize = surf.get_size()
        surfInString = pygame.image.tostring(surf, "RGBA", False)
        surfPIL = Image.frombytes("RGBA", surfSize, surfInString)

        # Blur image using PIL
        surfPILblurred = surfPIL.filter(ImageFilter.GaussianBlur(radius=blurRadius))

        # Convert it back to a pygame surface
        surf = pygame.image.fromstring(surfPILblurred.tobytes("raw", "RGBA"), surfSize, "RGBA")

        return (offset_x, offset_y, surf)
        
    def update(self) :

        previousActiveZones = list(self.activeZones)

        for zoneName, zone in self.zones.items() :
        
            inZone = self.heroInZone(zone)
            if (inZone) and (zoneName not in self.activeZones) :
                self.activeZones.append(zoneName)
            elif (not inZone) and (zoneName in self.activeZones) :
                self.activeZones.remove(zoneName)

        if (previousActiveZones != self.activeZones) :
            self.remakeGlobalOverlay()

    def heroInZone(self, zone) :
 
        heroX, heroY = shared.hero.position()

        heroX = int(heroX)
        heroY = int(heroY)

        w, h = zone["overlay"].get_size()
        cornerX, cornerY = zone["corner"]
        xOnSurf = int(heroX) - cornerX
        yOnSurf = int(heroY) - cornerY

        if (xOnSurf < 0) or (yOnSurf < 0) or (xOnSurf > w) or (yOnSurf > h) :
            return False

        pix = zone["overlay"].get_at((xOnSurf, yOnSurf))

        if (pix[0] > 127) :
            return True

        return False

    def render(self) :

        if (self.globalOverlay != None) :
            shared.view.blitRaw(self.globalOverlay, (0,0))

    def remakeGlobalOverlay(self) :
        
        # Prepare base surface

        globalW, globalH = shared.map.pixelSize()
        globalOverlay = pygame.Surface((globalW, globalH), flags=pygame.SRCALPHA)
        
        if (shared.debug) :
            globalOverlay.fill((30,30,30,230))
        else :
            globalOverlay.fill((30,30,30,255))

        # Draw all the active zone

        for zoneName in self.activeZones :

            x, y = self.zones[zoneName]["corner"]
            w, h = self.zones[zoneName]["overlay"].get_size()

            globalOverlay.blit(self.zones[zoneName]["overlay"], (x,y), special_flags=pygame.BLEND_RGBA_MIN)


        self.globalOverlay = globalOverlay


