import shared
from gameObjects.gameObject import GameObject
import ennemy

class SpawnMonster(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo, properties)

        if ("triggerGroup" not in self.properties) : 
            print("Warning ! Property triggerGroup is not set for object "+self.name)
            self.properties["triggerGroup"] = -1

        if ("monsterType" not in self.properties) : 
            print("Warning ! Property monsterType is not set for object "+self.name)
            self.properties["monsterType"] = None

        self.visible = False
        self.completed = False


    def trigger(self, source) :

        if not self.active : return
        self.active = False
        self.monster = ennemy.Ennemy(self.position())

        shared.ennemies.add(self.monster)
        self.completed = False

    def isCompleted(self) :

        if (not self.completed) and (not self.monster.alive) :
            self.completed = True
            self.monster = None
   
        return self.completed
