import pygame
import pygame.locals
import shared

from sets import Set
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


