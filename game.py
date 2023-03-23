import pygame, player, world, console
import constants.globals as globals
import constants.colors as colors
from pygame.locals import *
from typing import List

class Game():
    def __init__(self) -> None:
        pygame.display.set_caption(globals.SCREEN_CAPTION)
        self.surface = pygame.display.set_mode((globals.SCREEN_W, globals.SCREEN_H))
        self.clock = pygame.time.Clock()
        self.world = world.World(self.surface)
        self.player = player.Player(self.surface, 300, 500)
        self.console = console.Console(self.surface, self.player, self.world, self.clock)

    # React to events (input, etc)
    def processInput(self):
        for event in pygame.event.get():
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYDOWN)
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYUP)
            self.player.processQuitGameConditions(event)

    # Update game logic based on inputs
    def update(self, delta):
        self.player.updatePlayerPosition(delta, globals.H_SPEED, globals.V_SPEED, self.world.getQuadTree())

    # Render drawable objects
    def render(self):
        self.surface.fill(colors.BLACK)
        self.console.renderForDebug()
        self.world.renderTileSet()
        self.player.drawPlayer()
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