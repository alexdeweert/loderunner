import pygame
import sys
import constants.globals as globals
import constants.colors as colors
from pygame.locals import *
from typing import Optional

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = globals.PLAYER_W
        self.height = globals.PLAYER_H
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(colors.RED)
        self.rect = self.image.get_rect()
        self.playerKeysPressed = [False,False,False,False]
        self.prevX = self.rect.x
        self.prevY = self.rect.y
        self.xChangedPositive = False
        self.xChangedNegative = False
        self.yChangedPositive = False
        self.yChangedNegative = False
        
    def drawPlayer(self, screen: pygame.Surface):
        pygame.draw.rect(screen, colors.RED,  self.rect)

    def updatePlayerPosition(self,delta,hSpeed,vSpeed):
        resolvedHSpeed = delta * hSpeed
        resolvedVSpeed = delta * vSpeed
        # We might have to hack this and prevent diagonal movements when calculating vertical position.
        # I don't like that - because then this code isn't re-usable :\
        if(self.playerKeysPressed[globals.PressedKeys.LEFT]): self.rect.move_ip(-resolvedHSpeed, globals.ZERO)
        if(self.playerKeysPressed[globals.PressedKeys.RIGHT]): self.rect.move_ip(resolvedHSpeed, globals.ZERO)
        if(self.playerKeysPressed[globals.PressedKeys.UP]): self.rect.move_ip(globals.ZERO, -resolvedVSpeed)
        if(self.playerKeysPressed[globals.PressedKeys.DOWN]): self.rect.move_ip(globals.ZERO, resolvedVSpeed)
    
    def storePreviousPosition(self):
        self.prevX = self.rect.x
        self.prevY = self.rect.y

    def setDidMove(self):
        self.xChangedPositive = self.rect.x > self.prevX
        self.xChangedNegative = self.rect.x < self.prevX
        self.yChangedPositive = self.rect.y > self.prevY
        self.yChangedNegative = self.rect.y < self.prevY

    # This seems to work (at least when we're not using delta to scale movements, need to verify)
    def didMoveUp(self):
        return self.yChangedNegative
    def didMoveDown(self):
        return self.yChangedPositive
    def didMoveLeft(self):
        return self.xChangedNegative
    def didMoveRight(self):
        return self.xChangedPositive

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

    def resolvePositiveXCollision(self, withRect: pygame.Rect):
        if(withRect is not None):
            xDepth = self.getPositiveXDepth(withRect)
            self.rect.x = self.rect.x - xDepth

    def resolveNegativeXCollision(self, withRect: pygame.Rect):
        if(withRect is not None):
            xDepth = self.getNegativeXDepth(withRect)
            self.rect.x = self.rect.x - xDepth

    def resolvePositiveYCollision(self, withRect: pygame.Rect):
        if(withRect is not None):
            yDepth = self.getPositiveYDepth(withRect)
            self.rect.y = self.rect.y - yDepth
    
    def resolveNegativeYCollision(self, withRect: pygame.Rect):
        if(withRect is not None):
            yDepth = self.getNegativeYDepth(withRect)
            self.rect.y = self.rect.y - yDepth
    
    # Need to return the DIFFERENCE in the right and left rect borders.
    def getPositiveXDepth(self, rect: pygame.Rect) -> int :
        return self.rect.right - rect.left + 1
    
    # Need to return the DIFFERENCE in the right and left rect borders.
    def getNegativeXDepth(self, rect: pygame.Rect) -> int :
        return self.rect.left - rect.right - 1
        

     # Need to return the DIFFERENCE in the right and left rect borders.
    def getPositiveYDepth(self, rect: pygame.Rect) -> int :
        return self.rect.bottom - rect.top + 1
    
    # Need to return the DIFFERENCE in the right and left rect borders.
    def getNegativeYDepth(self, rect: pygame.Rect) -> int :
        return self.rect.top - rect.bottom - 1