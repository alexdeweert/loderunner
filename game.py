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
        self.tile = collidable.Collidable(200,200,32,32, True)
        self.cloud = collidable.Collidable(500,500,250,32, False)
        self.solidCollidableTileSet.append(self.tile)
        self.permeableCollidableTileSet.append(self.cloud)
        pygame.display.set_caption(globals.SCREEN_CAPTION)
        self.surface = pygame.display.set_mode((globals.SCREEN_W, globals.SCREEN_H))

    def renderFpsText(self):
        fpsString = str(int(self.clock.get_fps()))
        renderedFpsText = globals.DEBUG_FONT.render(fpsString, True, globals.DEBUG_FONT_COLOR)
        return renderedFpsText

    # React to events (input, etc)
    def processInput(self):
        for event in pygame.event.get():
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYDOWN)
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYUP)
            self.player.processQuitGameConditions(event)

    # Update game logic based on inputs
    def update(self, delta):
        self.player.updatePlayerPosition(delta, globals.H_SPEED, globals.V_SPEED, self.solidCollidableTileSet, self.permeableCollidableTileSet)

    # Render drawable objects
    def render(self):
        self.surface.fill(colors.BLACK)
        self.surface.blit(self.renderFpsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y))
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