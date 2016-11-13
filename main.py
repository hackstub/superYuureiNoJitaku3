import sys

if sys.version_info[0] == 3:
	import shared as s
else:
	import src.shared as s

from src import tileset, map, view, game, hero, ennemy, combatManager, visionManager

import pygame
from pygame.locals import *


def main() :

    s.tileset       = tileset.Tileset("assets/tileset/");

    s.view          = view.View("Test", (15,15))

    s.combatManager = combatManager.CombatManager()
    s.visionManager = visionManager.VisionManager()

    s.map           = map.Map("assets/map/map.json")
    s.hero          = hero.Hero("assets/sprites/hero.png")

    g               = game.Game()

    s.damageFont    = pygame.font.Font("./assets/fonts/bitdust2.ttf",14)
    
    while True :
        g.mainLoop()

main()

