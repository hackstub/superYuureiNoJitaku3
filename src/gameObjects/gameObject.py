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
        self.properties = properties

    def render(self) :

        if (self.active) and (self.visible) :
            shared.view.blit(self.tile, (self.x, self.y))

        elif (shared.debug) and (self.active) and (not self.visible) :
            shared.view.blit(self.tile, (self.x, self.y), debug=True)

    def trigger(self) :

        print "Object "+name+" got triggered !"


