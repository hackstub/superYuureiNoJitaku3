import shared
from gameObjects.gameObject import GameObject


class Trigger(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo)

        self.loadProperty(properties, "id", -1)

        self.visible = False


    def update(self) :

        if not self.active : 
            return False

        if (shared.distance(self.position(), shared.hero.position()) < shared.tileSize/4) :
            
            self.active = False
            
            for obj in shared.objectsInTriggerGroup(self.id) :
                obj.trigger(self)
    
        return True

