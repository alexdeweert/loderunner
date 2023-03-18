import pygame
import sys
import constants.globals as globals
import constants.colors as colors
import collidable
from pygame.locals import *
from typing import Optional
from typing import List

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
    def updatePlayerPosition(self, delta, hSpeed, vSpeed, withSolids: List[collidable.Collidable], withPermeables: List[collidable.Collidable]):
        deltaH = delta * hSpeed
        deltaV = delta * vSpeed
        self.storePreviousPosition()
        if self.hasValidLeftInput(): self.handleMove(-deltaH, globals.ZERO, withSolids, withPermeables)
        if self.hasValidRightInput(): self.handleMove(deltaH, globals.ZERO, withSolids, withPermeables)
        if self.hasValidUpInput(): self.handleMove(globals.ZERO, -deltaV, withSolids, withPermeables)
        if self.hasValidDownInput(): self.handleMove(globals.ZERO, deltaV, withSolids, withPermeables)
        self.setDidMove()

    def handleMove(self, deltaH: float, deltaV: float, withSolids: List[collidable.Collidable], withPermeables: List[collidable.Collidable]):
        for solid in withSolids:
            if not solid.willCollide(self.rect, deltaH, deltaV):
                self.rect.move_ip(deltaH, deltaV)
            else:
                # Else will collide so we don't allow movement, but we resolve it down to 1 pixel
                if deltaH > 0: self.resolveXGap(solid, solid.rect.left - self.rect.right, deltaV, 1)
                if deltaH < 0: self.resolveXGap(solid, self.rect.left - solid.rect.right, deltaV, -1)
                if deltaV > 0: self.resolveYGap(solid, solid.rect.top - self.rect.bottom, deltaH, 1)
                if deltaV < 0: self.resolveYGap(solid, self.rect.top - solid.rect.bottom, deltaH, -1)
        
        for permeable in withPermeables:
            permeable.didCollide(self.rect)
    
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

    def hasValidLeftInput(self):
        return self.playerKeysPressed[globals.PressedKeys.LEFT] and not self.playerKeysPressed[globals.PressedKeys.RIGHT]
    def hasValidRightInput(self):
        return self.playerKeysPressed[globals.PressedKeys.RIGHT] and not self.playerKeysPressed[globals.PressedKeys.LEFT]
    def hasValidUpInput(self):
        return self.playerKeysPressed[globals.PressedKeys.UP] and not self.playerKeysPressed[globals.PressedKeys.DOWN]
    def hasValidDownInput(self):
        return self.playerKeysPressed[globals.PressedKeys.DOWN] and not self.playerKeysPressed[globals.PressedKeys.UP]