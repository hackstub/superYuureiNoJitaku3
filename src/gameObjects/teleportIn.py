import shared
from gameObjects.gameObject import GameObject

class TeleportIn(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo, properties)

        if ("nameOut" not in self.properties) : 
            print("Warning ! Property id is not set for object "+self.name)
            self.properties["nameOut"] = -1

    def update(self) :

        if not self.active : 
            return False

        if (shared.distance(self.position(), shared.hero.position()) < shared.tileSize/2) :
            
            out = shared.searchObjectsByName(self.properties["nameOut"])
            if (len(out) != 1) :
                print("Error ! Cannot teleport ! Multiple or none out found !")
            
            x, y = out[0].position()
            shared.hero.x, shared.hero.y = x, y

        return False

