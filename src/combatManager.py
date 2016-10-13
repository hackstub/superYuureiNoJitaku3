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
        gameObjects = gameObjects.union(shared.ennemies)
        gameObjects = gameObjects.union(shared.projectiles)

        self.damageList = [ ]

        for obj in gameObjects :

            self.damageList.extend(obj.emmitDamage())
             
        for damage in self.damageList :
                
            damageSourceClass = damage.source.__class__.__name__

            for obj in gameObjects :

                objClass = obj.__class__.__name__

                if (damageSourceClass == objClass) :
                    continue

                if (shared.distance(damage.position, obj.position()) < damage.radius) :
                    
                    obj.receiveDamage(damage)

    def render(self) :
        
        for d in self.damageList :   

            shared.view.drawCircle((255,0,0,100),d.position,d.radius,1)

