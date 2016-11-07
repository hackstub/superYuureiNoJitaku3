import shared
from gameObject import GameObject
import ennemy

class SpawnMonster(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo, properties)

        if ("triggerId"   not in self.properties) : 
            print "Warning ! Property triggerId is not set for object "+self.name
            self.properties["triggerId"  ] = -1

        if ("monsterType" not in self.properties) : 
            print "Warning ! Property monsterType is not set for object "+self.name
            self.properties["monsterType"] = None

        self.visible = False


    def trigger(self, source) :

        if not self.active : return
        self.active = False

        shared.ennemies.add(ennemy.Ennemy(self.position()))
    
