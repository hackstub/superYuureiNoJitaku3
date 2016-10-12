import pygame
import pygame.locals
import shared

from sets import Set
from math import  sqrt

from ennemy import Ennemy

class EnnemyManager() :


    def __init__(self) :

        self.ennemies = Set()

    def add(self, pos) :

        e = Ennemy(pos)
        self.ennemies.add(e)

    def render(self) :

        for ennemy in self.ennemies :
            ennemy.render()

    def update(self) :

        for ennemy in self.ennemies :
            ennemy.update()

    def propagateAttackFromHero(self, hittedPositions) :

        for ennemy in self.ennemies :

            x, y = ennemy.x, ennemy.y

            for hitted_x, hitted_y in hittedPositions :

                Dx = abs(hitted_x - x)
                Dy = abs(hitted_y - y)

                if (Dx > shared.tileSize) or (Dy > shared.tileSize) :
                    continue

                r = sqrt(Dx*Dx + Dy*Dy)

                if (r < shared.tileSize) :
                    ennemy.gotHit()
                    break

                

