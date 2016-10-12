from math import sqrt
from sets import Set

tileSize               = 16

heroWalkingSpriteTempo = 4
heroWalkingSpeed       = 2
heroAttackSpriteTempo  = 2

ennemyWalkingSpeed     = 0.5
ennemyKnockBack        = tileSize



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

class Damage() :

    def __init__(self, source, position, radius, value) :
    
        self.source   = source
        self.position = position
        self.radius   = radius
        self.value    = value


projectiles = Set()
ennemies = Set()
