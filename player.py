import pygame
import sys
import constants.globals as globals
import constants.colors as colors
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = globals.PLAYER_W
        self.height = globals.PLAYER_H
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colors.RED)
        self.rect = self.image.get_rect()
        self.playerKeysPressed = [False,False,False,False]
        
    def drawPlayer(self, screen):
        pygame.draw.rect(screen, colors.RED,  self.rect)

    def updatePlayerPosition(self,delta,hSpeed,vSpeed):
        resolvedHSpeed = delta * hSpeed
        resolvedVSpeed = delta * vSpeed
        if(self.playerKeysPressed[globals.PressedKeys.LEFT]): self.rect.move_ip(-resolvedHSpeed, globals.ZERO)
        if(self.playerKeysPressed[globals.PressedKeys.RIGHT]): self.rect.move_ip(resolvedHSpeed, globals.ZERO)
        if(self.playerKeysPressed[globals.PressedKeys.UP]): self.rect.move_ip(globals.ZERO, -resolvedVSpeed)
        if(self.playerKeysPressed[globals.PressedKeys.DOWN]): self.rect.move_ip(globals.ZERO, resolvedVSpeed)

    def processMovementWithKeyEventTypes(self, event, eventType):
        if event.type == eventType:
            pressedValue = eventType == pygame.KEYDOWN
            if event.key == pygame.K_w:
                self.playerKeysPressed[globals.PressedKeys.UP] = pressedValue
            if event.key == pygame.K_s:
                self.playerKeysPressed[globals.PressedKeys.DOWN] = pressedValue
            if event.key == pygame.K_a:
                self.playerKeysPressed[globals.PressedKeys.LEFT] = pressedValue
            if event.key == pygame.K_d:
                self.playerKeysPressed[globals.PressedKeys.RIGHT] = pressedValue

    def processQuitGameConditions(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()