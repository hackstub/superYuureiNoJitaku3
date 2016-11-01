import shared

class GameObject() :

    def __init__(self, name, x, y, tileInfo, properties) :

        self.name       = name
        self.x          = x
        self.y          = y
        self.active     = True
        self.tileId     = tileInfo[0]
        self.tile       = tileInfo[1]
        self.properties = properties


    def render(self) :

        if (self.active) :
            shared.view.blitTile(self.tile, (self.x, self.y))

