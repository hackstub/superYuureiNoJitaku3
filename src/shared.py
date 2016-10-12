from math import sqrt

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

class Damage() :

    def __init__(self, source, position, radius, value) :
    
        self.source   = source
        self.position = position
        self.radius   = radius
        self.value    = value



