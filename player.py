import pygame
import sys
import constants.globals as globals
import constants.colors as colors
import collidable
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

    #TODO: Maybe make a Vector2 class (with an x and magnitude)
    def updatePlayerPosition(self, delta, hSpeed, vSpeed, withCollidable: collidable.Collidable):
        deltaH = delta * hSpeed
        deltaV = delta * vSpeed
        self.storePreviousPosition()
        if(self.playerKeysPressed[globals.PressedKeys.LEFT]): self.handleMove(-deltaH, globals.ZERO, withCollidable)
        if(self.playerKeysPressed[globals.PressedKeys.RIGHT]): self.handleMove(deltaH, globals.ZERO, withCollidable)
        if(self.playerKeysPressed[globals.PressedKeys.UP]): self.handleMove(globals.ZERO, -deltaV, withCollidable)
        if(self.playerKeysPressed[globals.PressedKeys.DOWN]): self.handleMove(globals.ZERO, deltaV, withCollidable)
        self.setDidMove()

    def handleMove(self, deltaH: float, deltaV: float, withCollidable: collidable.Collidable):
        '''
        The problem with this is that it does not solve tunnelling.
        That is, if the speed is fast enough, or if there's a large 
        delta due to game lag (luckily we cap that value) then willCollide
        will never return true and the movement will pass straight through.
        '''
        if not withCollidable.willCollide(self.rect, deltaH, deltaV):
            self.rect.move_ip(deltaH, deltaV)
        # Will collide so we don't allow movement, but we resolve it down to 1 pixel
        else:
            if deltaH > 0: self.resolveXGap(withCollidable, withCollidable.rect.left - self.rect.right, deltaV, 1)
            if deltaH < 0: self.resolveXGap(withCollidable, self.rect.left - withCollidable.rect.right, deltaV, -1)
            if deltaV > 0: self.resolveYGap(withCollidable, withCollidable.rect.top - self.rect.bottom, deltaH, 1)
            if deltaV < 0: self.resolveYGap(withCollidable, self.rect.top - withCollidable.rect.bottom, deltaH, -1)
    
    def resolveXGap(self, withCollidable: collidable.Collidable, distance: float, deltaV: float, dir: int):
        x = distance - 1
        if(x > 0): self.rect.move_ip(dir*x, deltaV)

    def resolveYGap(self, withCollidable: collidable.Collidable, distance: float, deltaH: float, dir: int):
        y = distance - 1
        if(y > 0): self.rect.move_ip(deltaH, dir*y)

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