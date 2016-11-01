from gameObject import GameObject

class SpawnMonster(GameObject) :


    def __init__(self, name, x, y, tileInfo, properties) :

        GameObject.__init__(self, name, x, y, tileInfo, properties)

        self.visible = False

