import shared
from sets import Set

class CombatManager() :


    def __init__(self) :

        pass

    def update(self) :

        gameObjects = Set() # TODO

        gameObjects.add(shared.hero)
        gameObjects = gameObjects.union(shared.ennemyManager.ennemies)

        damageList = [ ]

        for obj in gameObjects :

            damageList.extend(obj.emmitDamage())
             
        for damage in damageList :
                
            damageSourceClass = damage.source.__class__.__name__

            for obj in gameObjects :

                objClass = obj.__class__.__name__

                if (damageSourceClass == objClass) :
                    continue

                if (shared.distance(damage.position, obj.position()) < damage.radius) :
                    
                    obj.receiveDamage(damage)

                
