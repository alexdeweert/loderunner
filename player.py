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
        if(self.playerKeysPressed[globals.PressedKeys.LEFT]): self.rect.move_ip(-resolvedHSpeed, globals.ZERO)
        if(self.playerKeysPressed[globals.PressedKeys.RIGHT]): self.rect.move_ip(resolvedHSpeed, globals.ZERO)
        if(self.playerKeysPressed[globals.PressedKeys.UP]): self.rect.move_ip(globals.ZERO, -resolvedVSpeed)
        if(self.playerKeysPressed[globals.PressedKeys.DOWN]): self.rect.move_ip(globals.ZERO, resolvedVSpeed)
    
    def storePreviousPosition(self):
        self.prevX = self.rect.x
        self.prevY = self.rect.y

    def setDidMove(self):
        print(f"change in x: {self.rect.x - self.prevX}")
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

    # If its not none we collided with it
    def resolveXCollisionWith(self, rect: pygame.Rect):
        # We know a collision occured - so resolve the players position
        if(rect is not None):
            xDepth = self.getXDepth(rect)
            print(f"xDepth: {xDepth}")
            self.rect.x = self.rect.x - (xDepth+1)

    # If its not none we collided with it
    def resolveYCollisionWith(self, rect: pygame.Rect):
        # We know a collision occured - so resolve the players position
        if(rect is not None):
            yDepth = self.getYDepth(rect)
            print(f"yDepth: {yDepth}")
            self.rect.y = self.rect.y - (yDepth)
    
    # Need to return the DIFFERENCE in the right and left rect borders.
    def getXDepth(self, rect: pygame.Rect) -> int :
        if(self.rect.left < rect.left and self.rect.right > rect.left):
            return self.rect.right - rect.left
        
        if(self.rect.right > rect.right and self.rect.left < rect.right):
            return self.rect.left - rect.right
        
        return 0
        
    def getYDepth(self, rect: pygame.Rect) -> int :
        if(self.rect.top < rect.top and self.rect.bottom > rect.top):
            return self.rect.bottom - rect.top
        
        if(self.rect.bottom > rect.bottom and self.rect.top < rect.bottom):
            return self.rect.top - rect.bottom
        
        return 0