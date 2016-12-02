import shared
from gameObjects.gameObject import GameObject

class Door(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo)
   
        self.loadProperty(properties, "triggerGroups", "")
        self.loadProperty(properties, "state", False)

        self.visible = not self.state

    def render(self) :

        if (self.state == False) :
            shared.view.blit(self.tile, (self.x, self.y))

    def trigger(self, source) :

        self.state = not self.state
        self.visible = not self.state



