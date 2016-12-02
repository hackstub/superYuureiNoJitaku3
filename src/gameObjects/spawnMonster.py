import shared
from gameObjects.gameObject import GameObject
import ennemy

class SpawnMonster(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo)

        self.loadProperty(properties, "triggerGroups", "")
        self.loadProperty(properties, "monsterType", "")

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
