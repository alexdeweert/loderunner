import constants.globals as globals
import constants.colors as colors
import pygame, player, world

class Console():
    def __init__(self, surface: pygame.Surface, player: player.Player, world: world.World, clock: pygame.time.Clock) -> None:
        self.surface = surface
        self.player = player
        self.world = world
        self.clock = clock

    def renderForDebug(self):
        if globals.DEBUG:
            self.world.renderQuadTree()
            self.surface.blit(self.__renderFpsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y))
            self.surface.blit(self.__renderCollisionsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y + 16))
            self.surface.blit(self.__renderPlayerPositionText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y + 32))
            self.surface.blit(self.__renderOnFloorState(), (globals.FPS_DISP_X, globals.FPS_DISP_Y + 48))
            self.surface.blit(self.__renderLadderState(), (globals.FPS_DISP_X, globals.FPS_DISP_Y + 64))

    def __renderFpsText(self):
        fpsString = f"fps: {str(int(self.clock.get_fps()))}"
        renderedFpsText = globals.DEBUG_FONT.render(fpsString, True, globals.DEBUG_FONT_COLOR)
        return renderedFpsText
    
    def __renderCollisionsText(self):
        bruteForceCollisions = f"collisions: {str(self.player.collisionsCalculated)}"
        renderedBruteForceCollisions = globals.DEBUG_FONT.render(bruteForceCollisions, True, globals.DEBUG_FONT_COLOR)
        return renderedBruteForceCollisions
    
    def __renderPlayerPositionText(self):
        playerPosition = f"PlayerX: {str(self.player.rect.x)}, PlayerY: {str(self.player.rect.y)}"
        return globals.DEBUG_FONT.render(playerPosition, True, globals.DEBUG_FONT_COLOR)
    
    def __renderOnFloorState(self):
        onFloorText = f"onFloor: {str(self.player.onFloor)}"
        return globals.DEBUG_FONT.render(onFloorText, True, globals.DEBUG_FONT_COLOR)
    
    def __renderLadderState(self):
        onFloorText = f"touchingLadder: {str(self.player.touchingLadder)}, onLadder: {str(self.player.onLadder)}, onRope: {str(self.player.onRope)}"
        return globals.DEBUG_FONT.render(onFloorText, True, globals.DEBUG_FONT_COLOR)