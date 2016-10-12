
from src import shared as s
from src import game, map, view, hero, tileset, ennemyManager


def main() :

    s.tileset       = tileset.Tileset("assets/tileset.png", "assets/tileset_mask.png");
    
    s.map           = map.Map("assets/map.json")
    s.hero          = hero.Hero("assets/hero.png")
    
    s.ennemyManager = ennemyManager.EnnemyManager()
    s.ennemyManager.add((40,40))
    s.ennemyManager.add((100,30))
    
    s.view          = view.View("Test", (10,9))
    
    g               = game.Game();
    
    while True :
        g.mainLoop()

main()
