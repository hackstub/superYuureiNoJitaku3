
import shared as s
import tileset, map, view, game, hero, combatManager, visionManager
import pygame
from pygame.locals import *


from combatManager import CombatManager
from visionManager import VisionManager

def main() :

    s.tileset       = tileset.Tileset("assets/tileset/");
    
    s.view          = view.View("Test", (20,20))
    
    s.combatManager = combatManager.CombatManager()
    s.visionManager = visionManager.VisionManager()

    s.map           = map.Map("assets/map/map.json")
    s.hero          = hero.Hero("assets/sprites/hero.png")
    
    g               = game.Game()
        
    s.damageFont    = pygame.font.Font("./assets/fonts/bitdust2.ttf",14)
    
    while True :
        g.mainLoop()

main()
