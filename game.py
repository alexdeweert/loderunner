import pygame, sys, player, collidable
import constants.globals as globals
import constants.colors as colors
from pygame.locals import *
from enum import IntEnum
from typing import List

class Game():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.player = player.Player()
        self.solidCollidableTileSet: List[collidable.Collidable] = list()
        self.permeableCollidableTileSet: List[collidable.Collidable] = list()

        width = 0
        while(width <= (globals.SCREEN_W - 32)):
            self.solidCollidableTileSet.append(collidable.Collidable(width,700,32,16, True, colors.GREEN, colors.BLUE))
            width += 32
        self.permeableCollidableTileSet.append(collidable.Collidable(10,50,163,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(84,125,80,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(148,175,163,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(300,125,163,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(394,40,100,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(560,145,163,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(650,64,75,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(780,150,180,32, False, colors.WHITE, colors.GRAY))

        pygame.display.set_caption(globals.SCREEN_CAPTION)
        self.surface = pygame.display.set_mode((globals.SCREEN_W, globals.SCREEN_H))

    def renderFpsText(self):
        fpsString = f"fps: {str(int(self.clock.get_fps()))}"
        renderedFpsText = globals.DEBUG_FONT.render(fpsString, True, globals.DEBUG_FONT_COLOR)
        
        return renderedFpsText
    
    def renderCollisionsText(self):
        bruteForceCollisions = f"collisions: {str(self.player.collisionsCalculated)}"
        renderedBruteForceCollisions = globals.COLLISIONS_FONT.render(bruteForceCollisions, True, globals.DEBUG_FONT_COLOR)
        return renderedBruteForceCollisions


    # React to events (input, etc)
    def processInput(self):
        for event in pygame.event.get():
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYDOWN)
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYUP)
            self.player.processQuitGameConditions(event)

    # Update game logic based on inputs
    def update(self, delta):
        '''
        TODO: We want to add and remove collidable tiles (and permeable tiles) only if they're in the same quadrant as the player
        otherwise they should be removed from the list to check.
        There should be a single quad tree, and as the player moves it's position within the tree will be updated.
        All static items during initial population (and during dynamic creation/destruction during gamerplay) will be
        added to the quad tree.
        '''
        self.player.updatePlayerPosition(delta, globals.H_SPEED, globals.V_SPEED, self.solidCollidableTileSet, self.permeableCollidableTileSet)

    # Render drawable objects
    def render(self):
        self.surface.fill(colors.BLACK)
        self.surface.blit(self.renderFpsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y))
        self.surface.blit(self.renderCollisionsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y + 16))
        self.player.drawPlayer(self.surface)
        # TODO: move tilesets logic to world class
        for solidTile in self.solidCollidableTileSet:
            solidTile.draw(self.surface)
        for permeableTile in self.permeableCollidableTileSet:
            permeableTile.draw(self.surface)
        pygame.display.flip()
        
    def run(self):
        while True:
            delta = self.clock.tick(globals.FPS) / globals.SECOND_MS
            pygame.time.delay(globals.SIMULATED_LAG_MS)
            if(delta > globals.MAX_DELTA):
                delta = globals.MAX_DELTA
            self.processInput()
            self.update(delta)
            self.render()

if __name__ == '__main__':
    pygame.init()
    globals.init()
    colors.init()
    Game().run()