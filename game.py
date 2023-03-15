import pygame, sys, globals, player
from pygame.locals import *
from enum import IntEnum

class Game():
    def __init__(self) -> None:
        self.display = pygame.display
        self.time = pygame.time
        self.clock = self.time.Clock()
        self.player = player.Player()
        self.display.set_caption(globals.SCREEN_CAPTION)
        self.screen = self.display.set_mode((globals.SCREEN_W, globals.SCREEN_H))
        self.keysPressed = [False,False,False,False]

    def renderFpsText(self):
        fpsString = str(int(self.clock.get_fps()))
        renderedFpsText = globals.DEBUG_FONT.render(fpsString, True, globals.DEBUG_FONT_COLOR)
        return renderedFpsText

    # React to events (input, etc)
    def processInputAndEvents(self):
        for event in pygame.event.get():
            self.processMovementWithKeyEventTypes(event, pygame.KEYDOWN)
            self.processMovementWithKeyEventTypes(event, pygame.KEYUP)
            self.processQuitGameConditions(event)

    def processMovementWithKeyEventTypes(self, event, eventType):
        if event.type == eventType:
            pressedValue = eventType == pygame.KEYDOWN
            if event.key == pygame.K_w:
                self.keysPressed[globals.PressedKeys.UP] = pressedValue
            if event.key == pygame.K_s:
                self.keysPressed[globals.PressedKeys.DOWN] = pressedValue
            if event.key == pygame.K_a:
                self.keysPressed[globals.PressedKeys.LEFT] = pressedValue
            if event.key == pygame.K_d:
                self.keysPressed[globals.PressedKeys.RIGHT] = pressedValue

    def processQuitGameConditions(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update game logic based on inputs
    def update(self, delta):
        self.player.updatePlayerPosition(delta, globals.H_SPEED, globals.V_SPEED, self.keysPressed)

    # Render drawable objects
    def render(self):
        # On each loop fill the entire canvas with one color
        self.screen.fill((0,0,0))

        # Draw to the canvas
        self.screen.blit(self.renderFpsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y))
        self.player.drawPlayer(self.screen)
        self.display.flip()
        
    def run(self):
        while True:
            delta = self.clock.tick(globals.FPS) / 1000
            
            # Limit the delta, in case of huge amounts of lag
            if(delta > globals.MAX_DELTA):
                delta = globals.MAX_DELTA

            # Process Input
            self.processInputAndEvents()
            # Update
            self.update(delta)
            # Render
            self.render()

if __name__ == '__main__':
    pygame.init()
    globals.init()
    Game().run()