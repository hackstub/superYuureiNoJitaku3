from gameObjects.gameObject import GameObject

class SpawnHero(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo)
    
        self.visible = False


