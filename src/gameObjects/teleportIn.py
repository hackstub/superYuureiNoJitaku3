import shared
from gameObjects.gameObject import GameObject

class TeleportIn(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo)

        self.loadProperty(properties, "nameOut", "")

    def update(self) :

        if not self.active : 
            return False

        if (shared.distance(self.position(), shared.hero.position()) < shared.tileSize/2) :
            
            out = shared.searchObjectByName(self.nameOut)
            x, y = out.position()
            shared.hero.x, shared.hero.y = x, y

        return False

