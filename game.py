import pygame, sys, player
import constants.globals as globals
import constants.colors as colors
from pygame.locals import *
from enum import IntEnum

class Game():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.player = player.Player()
        pygame.display.set_caption(globals.SCREEN_CAPTION)
        self.screen = pygame.display.set_mode((globals.SCREEN_W, globals.SCREEN_H))

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
        self.player.updatePlayerPosition(delta, globals.H_SPEED, globals.V_SPEED)

    # Render drawable objects
    def render(self):
        # On each loop fill the entire canvas with one color
        self.screen.fill(colors.BLACK)

        # Draw to the canvas
        self.screen.blit(self.renderFpsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y))
        self.player.drawPlayer(self.screen)
        pygame.display.flip()
        
    def run(self):
        while True:
            delta = self.clock.tick(globals.FPS) / globals.SECOND_MS
            
            # Limit the delta, in case of huge amounts of lag
            if(delta > globals.MAX_DELTA):
                delta = globals.MAX_DELTA

            # Process Input
            self.processInput()
            # Update
            self.update(delta)
            # Render
            self.render()

if __name__ == '__main__':
    pygame.init()
    globals.init()
    colors.init()
    Game().run()