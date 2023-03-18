import pygame, sys, player, collidable
import constants.globals as globals
import constants.colors as colors
from pygame.locals import *
from enum import IntEnum

class Game():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.player = player.Player()
        self.tile = collidable.Collidable(40,40,32,32)
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
        print(f"didMoveUp {self.player.didMoveUp()}, didMoveDown: {self.player.didMoveDown()}, didMoveLeft: {self.player.didMoveLeft()}, didMoveRight: {self.player.didMoveRight()}")
        self.player.updatePlayerPosition(delta, globals.H_SPEED, globals.V_SPEED)
        self.player.setDidMove()
        if self.player.didMoveRight():
            self.player.resolvePositiveXCollision(self.tile.didCollide(self.player.rect))
        if self.player.didMoveLeft():
            self.player.resolveNegativeXCollision(self.tile.didCollide(self.player.rect))
        if self.player.didMoveDown():
            self.player.resolvePositiveYCollision(self.tile.didCollide(self.player.rect))
        if self.player.didMoveUp():
            self.player.resolveNegativeYCollision(self.tile.didCollide(self.player.rect))
        self.player.storePreviousPosition()
        
            

    # Render drawable objects
    def render(self):
        # On each loop fill the entire canvas with one color
        self.surface.fill(colors.BLACK)
        self.surface.blit(self.renderFpsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y))
        self.player.drawPlayer(self.surface)
        self.tile.draw(self.surface)

        pygame.display.flip()
        
    def run(self):
        while True:
            delta = self.clock.tick(globals.FPS) / globals.SECOND_MS
            #pygame.time.delay(50)
            # Limit the delta, in case of huge amounts of lag
            if(delta > globals.MAX_DELTA):
                delta = globals.MAX_DELTA

            # Process Input
            self.processInput()
            # Update
            self.update(1)
            # Render
            self.render()

if __name__ == '__main__':
    pygame.init()
    globals.init()
    colors.init()
    Game().run()