import shared


class GameObject() :

    def __init__(self, name, x, y, tileInfo, properties) :

        self.name       = name
        self.x          = (x + 0.5) * shared.tileSize
        self.y          = (y + 0.5) * shared.tileSize
        self.active     = True
        self.visible    = True
        self.tileId     = tileInfo[0]
        self.tile       = tileInfo[1]
        
        if (properties == None) : self.properties = {}
        else                    : self.properties = properties


    def position(self) :

        return (self.x, self.y)

    def render(self) :

        if (self.active) and (self.visible) :
            shared.view.blit(self.tile, (self.x, self.y))

        elif (shared.debug) and (self.active) and (not self.visible) :
            shared.view.blit(self.tile, (self.x, self.y), debug=True)

    def update(self) :

        pass

    def trigger(self, source) :

        print("Object "+self.name+" got triggered !")
    
    def isCompleted(self) :

        return True


