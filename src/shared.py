from math import sqrt

import importlib
import pygame
from pygame.locals import *


tileSize               = 32

heroWalkingSpriteTempo = 4
heroWalkingSpeed       = int(tileSize / 8)
heroAttackSpriteTempo  = 2

ennemyWalkingSpeed     = 1
ennemyKnockBack        = int(tileSize / 3)

debug = False
#debug = True

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

    if not (map.isWalkable(source.mask(), pos)) : 
        return False

    if ((source != hero) 
    and (hero not in ignoreList)
    and (distance(hero.position(), pos) < tileSize)) : 
        return False 
    
    if not (ignoreEnnemies) :
        for ennemy in ennemies :
            if  ((source != ennemy)
            and  (ennemy not in ignoreList)
            and  (ennemy.alive)
            and  (distance(ennemy.position(), pos) < tileSize)) : 
                return False

    return True

def objectsInTriggerGroup(id) :

    L = []

    for obj in map.layer["objects"] :
        if (type(obj) == int) : continue
        if (not hasattr(obj, "triggerGroups")) : continue
        if (id not in obj.triggerGroups) : continue

        L.append(obj)

    return L

def searchObjectByName(name) :

    for obj in map.layer["objects"] :
        if (type(obj) == int) : continue
        if (obj.name == name) : 
            return obj


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



projectiles = set()
ennemies = set()
