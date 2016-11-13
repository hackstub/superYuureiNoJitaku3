import shared
from gameObjects.gameObject import GameObject

class Door(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo, properties)

        if ("triggerGroup" not in self.properties) : 
            print("Warning ! Property triggerGroup is not set for object "+self.name)
            self.properties["triggerGroup"] = -1

        if ("state" not in self.properties) : 
            print("Warning ! Property state is not set for object "+self.name)
            self.properties["state"] = False

    def render(self) :

        if (self.properties["state"] == False) :
            shared.view.blit(self.tile, (self.x, self.y))

    def trigger(self, source) :

        self.properties["state"] = not self.properties["state"] 






