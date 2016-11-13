import shared
from gameObjects.gameObject import GameObject


class Trigger(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo, properties)

        if ("id" not in self.properties) : 
            print("Warning ! Property id is not set for object "+self.name)
            self.properties["id"] = -1

        self.visible = False


    def update(self) :

        if not self.active : 
            return

        if (shared.distance(self.position(), shared.hero.position()) < shared.tileSize/2) :
            
            self.active = False
            
            for obj in shared.searchObjectsByProperty("triggerGroup", self.properties["id"]) :
                obj.trigger(self)

