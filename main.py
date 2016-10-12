
from src import shared as s
from src import game, map, view, character, tileset, ennemyManager


def main() :

    s.tileSize      = 16
    s.tileset       = tileset.Tileset("assets/tileset.png", "assets/tileset_mask.png");
    
    s.map           = map.Map("assets/map.json")
    s.hero          = character.Character("assets/hero.png")
    
    s.ennemyManager = ennemyManager.EnnemyManager()
    s.ennemyManager.add((40,40))
    
    s.ennemyManager.add((60,80))
    
    s.view          = view.View("Test", (9,10))
    
    g               = game.Game();
    
    while True :
        g.mainLoop()

main()
