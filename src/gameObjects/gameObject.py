import shared


class GameObject() :

    def __init__(self, name, x, y, tileInfo) :

        self.name       = name
        self.x          = (x + 0.5) * shared.tileSize
        self.y          = (y + 0.5) * shared.tileSize
        self.active     = True
        self.visible    = True
        self.tileId     = tileInfo[0]
        self.tile       = tileInfo[1]
        

    def loadProperty(self, properties, name, defaultValue) :

        if (properties == None) : properties = {}

        if (name not in properties.keys()) :
            print("Warning ! Property "+name+" is not set for object "+self.name)
            properties[name] = defaultValue
       
        if (name == "triggerGroups") :
            if (properties[name] == "") :
                properties[name] = []
            else :
                properties[name] = [ int(i) for i in properties[name].replace(" ", "").split(",") ]

        setattr(self, name, properties[name])

    def position(self) :

        return (self.x, self.y)

    def render(self) :

        if (self.active) and (self.visible) :
            shared.view.blit(self.tile, (self.x, self.y))

        elif (shared.debug) and (self.active) and (not self.visible) :
            shared.view.blit(self.tile, (self.x, self.y), debug=True)

    def update(self) :

        return False

    def trigger(self, source) :

        print("Object "+self.name+" got triggered !")
    
    def isCompleted(self) :

        return True


