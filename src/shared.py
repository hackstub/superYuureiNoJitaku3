from math import sqrt
from sets import Set

import importlib
import pygame
from pygame.locals import *


tileSize               = 32

heroWalkingSpriteTempo = 4
heroWalkingSpeed       = tileSize / 8
heroAttackSpriteTempo  = 2

ennemyWalkingSpeed     = tileSize / 32
ennemyKnockBack        = tileSize / 3

#debug = False
debug = True

def distance(pos1, pos2) :
    
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]

    return sqrt(dx*dx+dy*dy)

def directionToVector(d, mag) :

    if (d == "back" ) or (d == "up"  ) : return (0, -mag)
    if (d == "front") or (d == "down") : return (0, +mag)
    if (d == "left" ) :                  return (-mag, 0)
    if (d == "right") :                  return (+mag, 0)

    return (0,0)


def strToObjectClass(className):

    moduleName = "gameObjects."+className[0].lower() + className[1:]

    m = importlib.import_module(moduleName)
    
    c = getattr(m, className)

    return c

def isWalkable(source, pos, ignoreEnnemies = False, ignoreList = [ ]) :

    if not (map.isWalkable(pos)) : 
        return False

    if ((source != hero) 
    and (hero not in ignoreList)
    and (distance(hero.position(), pos) < tileSize)) : 
        return False 
    
    if not (ignoreEnnemies) :
        for ennemy in ennemies :
            if  ((source != ennemy)
            and  (ennemy not in ignoreList)
            and  (distance(ennemy.position(), pos) < tileSize)) : 
                return False

    return True


def makeMaskFromPolygon(vertices, blurRadius = 10) :
    
    from PIL import Image, ImageFilter
    
    base = pygame.Surface((2000,2000), flags=SRCALPHA)
    base.fill((0,0,0,0))

    offseted_vertices = [ (x+1000,y+1000) for x,y in vertices ]
    rect = pygame.draw.polygon(base, (255,255,255,255), offseted_vertices)
  
    margin = 25

    surf = base.subsurface((rect.x     -   margin, rect.y      -   margin,
                            rect.width + 2*margin, rect.height + 2*margin))
    
    offset_x, offset_y = 1000-rect.x+margin, 1000-rect.y+margin
    

    # convert surf to PIL image
    surf_size = surf.get_size()
    surf_in_string = pygame.image.tostring(surf, "RGBA", False)
    pil_image = Image.frombytes("RGBA",surf_size, surf_in_string)

    # blur image
    pil_blured = pil_image.filter(ImageFilter.GaussianBlur(radius=blurRadius))

    # convert it back to a pygame surface
    surf = pygame.image.fromstring(pil_blured.tobytes("raw", "RGBA"), surf_size, "RGBA")

    return ((offset_x, offset_y), surf)

def makeMask(size, maskList) :

    globalW, globalH = size
    base = pygame.Surface((globalW, globalH), flags=SRCALPHA)
    base.fill((0,0,0,255))
    
    for x,y, mask in maskList :

        w, h = mask.get_size() 
        
        for i in range(0,w) :
            for j in range(0,h) :
                m = mask.get_at((i,j))
                b = base.get_at((x+i,y+j))
                a = b[3] - m[0]
                if (a < 0) : a = 0
                b = base.set_at((x+i,y+j), (b[0], b[1], b[2], a))

    return base

class Damage() :

    def __init__(self, source, position, radius, value) :
    
        self.source   = source
        self.position = position
        self.radius   = radius
        self.value    = value

    def makeDamageText(self, insideColor = (255,255,255), outsideColor=(0,0,0)) :

        textIn   = damageFont.render(str(self.value), 1, insideColor )
        textOut  = damageFont.render(str(self.value), 1, outsideColor)
        size = textIn.get_width() + 2, textIn.get_height() + 2
        s = pygame.Surface(size, pygame.SRCALPHA, 32)
        s.blit(textOut,(0,0))    
        s.blit(textOut,(2,2))    
        s.blit(textOut,(2,0))    
        s.blit(textOut,(0,2))    
        s.blit(textIn, (1,1))    

        return s



projectiles = Set()
ennemies = Set()
