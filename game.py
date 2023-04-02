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
        self.player = player.Player(self.surface, 300, 500, globals.PLAYER_W, globals.PLAYER_H, self.world.getQuadTree())
        self.console = console.Console(self.surface, self.player, self.world, self.clock)

    # React to events (input, etc)
    '''
    Need to determine where to draw clicks.
    The mouse can click on 0->32, 33->64
    When we detect clicks we want to create a rect at the (mouse position // 32) * 32 (maybe)
    ie mouse click at x = 15, then (15//32 == 0) * 32 = 0.
    mouse click x = 33, then (33//32 = 1) * 32 = 32
    '''
    def processInput(self):
        for event in pygame.event.get():
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYDOWN)
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYUP)
            self.player.processQuitGameConditions(event)
            # Create a block wherever we click (TODO: Move this to an editor class)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.world.insertFloorPieceIntoWorld(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                print(f"mouse: {pygame.mouse.get_pos()}")
    # Update game logic based on inputs
    def update(self, delta):
        self.player.update(delta)

    # Render drawable objects
    def render(self):
        self.surface.fill(colors.BLACK)
        self.console.renderForDebug()
        self.world.renderTileSet()
        self.player.draw()
        # Render grid (TODO: Move this to an editor class)
        for i in range(32, globals.SCREEN_W, 32):
            pygame.draw.line(self.surface, colors.DARK_GRAY, (i,0), (i,globals.SCREEN_H))
            pygame.draw.line(self.surface, colors.DARK_GRAY, (0,i), (globals.SCREEN_W,i))
        pygame.display.flip()
        
    def run(self):
        while True:
            delta = self.clock.tick(globals.FPS) / globals.SECOND_MS
            pygame.time.delay(globals.SIMULATED_LAG_MS)
            if(delta > globals.MAX_DELTA):
                delta = globals.MAX_DELTA
            self.processInput()
            self.update(1)
            self.render()

if __name__ == '__main__':
    pygame.init()
    globals.init()
    colors.init()
    Game().run()