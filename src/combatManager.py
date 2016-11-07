import pygame
import pygame.locals
import shared
from sets import Set

class CombatManager() :


    def __init__(self) :

        pass

    def update(self) :

        gameObjects = Set() # TODO

        gameObjects.add(shared.hero)
        gameObjects = gameObjects.union(shared.projectiles)
        for ennemy in shared.ennemies :
            if (not ennemy.alive) : continue
            gameObjects.add(ennemy)

        self.damageList = [ ]

        for obj in gameObjects :

            self.damageList.extend(obj.emmitDamage())
             
        for damage in self.damageList :
                
            for obj in gameObjects :

                if (obj == damage.source) : continue

                if (shared.distance(damage.position, obj.position()) < damage.radius) :
                    
                    obj.receiveDamage(damage)
                    damage.source.dealtDamage(obj)

    def render(self) :
        
        for d in self.damageList :   

            shared.view.drawCircle((255,0,0,100),d.position,d.radius,1)

