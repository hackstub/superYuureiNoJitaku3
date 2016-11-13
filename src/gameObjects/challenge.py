import shared
from gameObjects.gameObject import GameObject

class Challenge(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo, properties)

        if ("id" not in self.properties) : 
            print("Warning ! Property id is not set for object "+self.name)
            self.properties["id"] = -1

        if ("triggerInitId" not in self.properties) : 
            print("Warning ! Property triggerInitId is not set for object "+self.name)
            self.properties["triggerInitId"] = -1

        if ("triggerCompletionId" not in self.properties) : 
            print("Warning ! Property triggerCompletionId is not set for object "+self.name)
            self.properties["triggerCompletionId"] = -1

        self.visible = False
        self.ongoing = False

    def update(self) :

        if not self.active : 
            return

        if (self.ongoing) :

            id_ = self.properties["triggerInitId"] 
            
            for obj in shared.searchObjectsByProperty("triggerGroup", self.properties["triggerInitId"]) :
                if (not obj.isCompleted()) : return

            for obj in shared.searchObjectsByProperty("triggerGroup", self.properties["id"]) :
                obj.trigger(self)

            self.active = False

            return

        if (shared.distance(self.position(), shared.hero.position()) < shared.tileSize/2) :
            
            self.ongoing = True
            
            for obj in shared.searchObjectsByProperty("triggerGroup", self.properties["triggerInitId"]) :
                obj.trigger(self)


