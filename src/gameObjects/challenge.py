import shared
from gameObjects.gameObject import GameObject

class Challenge(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo)

        self.loadProperty(properties, "id", -1)
        self.loadProperty(properties, "triggerInitId", -1)
        self.loadProperty(properties, "triggerCompletionId", -1)

        self.visible = False
        self.ongoing = False

    def update(self) :

        if not self.active : 
            return False

        if (self.ongoing) :

            for obj in shared.objectsInTriggerGroup(self.triggerInitId) :
                if (not obj.isCompleted()) : return False

            for obj in shared.objectsInTriggerGroup(self.triggerCompletionId) :
                obj.trigger(self)

            self.active = False

            return True

        if (shared.distance(self.position(), shared.hero.position()) < shared.tileSize/4) :
            
            self.ongoing = True
            
            for obj in shared.objectsInTriggerGroup(self.triggerInitId) :
                obj.trigger(self)

            return True

        return False


