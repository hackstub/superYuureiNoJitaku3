import sys

import pygame
import pygame.locals
import shared

from combatManager import CombatManager

class Game() : 


    def __init__(self) :

        # Initialize PyGame
        pygame.init()
  
        # Set up FPS clock
        self.fps = 30
        self.fpsClock = pygame.time.Clock()

        self.combatManager = CombatManager()

    def mainLoop(self) :

        # Handle events
        self.eventHandler()

        # Handle keys
        self.keysHandler()

        # Update stuff
        shared.hero.update()
        shared.ennemyManager.update()
        self.combatManager.update()

        # Render stuff
        shared.view.reset()

        shared.map.render()
        shared.ennemyManager.render()
        shared.hero.render()

        # Update screen
        pygame.display.update()
        self.fpsClock.tick(self.fps)
        

    def eventHandler(self) :

        for event in pygame.event.get():

            if (event.type == pygame.QUIT) :
                pygame.quit()
                sys.exit()


    def keysHandler(self) :
        
        keyPressed = pygame.key.get_pressed()

        moveDirection = ""
        if (keyPressed[pygame.K_UP])    : moveDirection = "back"
        if (keyPressed[pygame.K_DOWN])  : moveDirection = "front"
        if (keyPressed[pygame.K_LEFT])  : moveDirection = "left"
        if (keyPressed[pygame.K_RIGHT]) : moveDirection = "right"

        if (moveDirection != "") :
            shared.hero.look(moveDirection)
            shared.hero.move(moveDirection)

        if (keyPressed[pygame.K_e]) :
            shared.hero.attackKeyHandler()



