import shared
from gameObject import GameObject


class Trigger(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo, properties)

        if ("id" not in self.properties) : 
            print "Warning ! Property id is not set for object "+self.name
            self.properties["id"] = -1

        self.visible = False


    def update(self) :

        if not self.active : 
            return

        if (shared.distance(self.position(), shared.hero.position()) < shared.tileSize/2) :
            
            self.active = False
            
            id_ = self.properties["id"] 
            if (id_ == -1) : return

            for obj in shared.map.layer["objects"] :
                if (type(obj) == int) : continue
                if ("triggerId" not in obj.properties) : continue
                if (obj.properties["triggerId"] != id_) : continue
            
                obj.trigger(self)

