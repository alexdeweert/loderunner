import pygame
import sys
import constants.globals as globals
import constants.colors as colors
import collidable
import quadtreenode
from pygame.locals import *
from typing import Optional
from typing import List

class Player(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, x: int, y: int) -> None:
        super().__init__()
        self.surface = surface
        self.width = globals.PLAYER_W
        self.height = globals.PLAYER_H
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((colors.RED))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.playerKeysPressed = [False,False,False,False]
        self.prevX = self.rect.x
        self.prevY = self.rect.y
        self.xChangedPositive = False
        self.xChangedNegative = False
        self.yChangedPositive = False
        self.yChangedNegative = False
        self.collisionsCalculated = 0
        self.quadTreeCollisisionCalculated = 0
        self.onFloor = False
        self.onLadder = False
        self.touchingLadder = False
        self.onRope = False
        
    def drawPlayer(self):
        pygame.draw.rect(self.surface, colors.RED,  self.rect)

    def updatePlayerPosition(self, delta, hSpeed, vSpeed, quadTree: quadtreenode.QuadTreeNode):
        deltaH = delta * hSpeed
        deltaV = delta * vSpeed
        gravity = delta * globals.GRAVITY_SPEED
        self.__storePreviousPosition()
        if self.__hasValidLeftInput(): self.__handleMove(-deltaH, globals.ZERO, delta, quadTree)
        if self.__hasValidRightInput(): self.__handleMove(deltaH, globals.ZERO, delta,quadTree)
        if self.__hasValidUpInput(): self.__handleMove(globals.ZERO, -deltaV, delta,quadTree)
        if self.__hasValidDownInput(): self.__handleMove(globals.ZERO, deltaV, delta,quadTree)
        if not self.onLadder: self.__handleMove(globals.ZERO, gravity, delta, quadTree)
        self.__setDidMove()
    
    # Not used at the moment, could use later though.
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

    def __handleMove(self, deltaH: float, deltaV: float, delta: float, quadTree: quadtreenode.QuadTreeNode):
        if globals.DEBUG: self.__checkQuadTreeCollisionsForDraw(quadTree)
        willNotCollide = True
        collidables = self.__findSolidsInQuadTree(quadTree, [], set([]))
        self.onLadder = False
        self.onFloor = False
        for collidable in collidables:
            self.collisionsCalculated = self.collisionsCalculated + 1
            if collidable.isSolid:
                if collidable.willCollide(self.rect, deltaH, deltaV):
                    self.onFloor = collidable.isFloor
                    if deltaH > 0: self.__resolveXGap(collidable, collidable.rect.left - self.rect.right, deltaV, 1)
                    if deltaH < 0: self.__resolveXGap(collidable, self.rect.left - collidable.rect.right, deltaV, -1)
                    if deltaV > 0: self.__resolveYGap(collidable, collidable.rect.top - self.rect.bottom, deltaH, 1)
                    if deltaV < 0: self.__resolveYGap(collidable, self.rect.top - collidable.rect.bottom, deltaH, -1)
                    willNotCollide = False
            elif collidable.didCollide(self.rect) and collidable.isLadder:
                self.onLadder = True
                self.onFloor = False

                
        if willNotCollide:
            self.rect.move_ip(deltaH, deltaV)
        
    
    def __resolveXGap(self, withCollidable: collidable.Collidable, distance: float, deltaV: float, dir: int):
        # Resolve gap down to one pixel
        x = distance - 1
        if(x > 0): self.rect.move_ip(dir*x, deltaV)

    def __resolveYGap(self, withCollidable: collidable.Collidable, distance: float, deltaH: float, dir: int):
        # Resolve gap down to one pixel
        y = distance - 1
        if(y > 0): self.rect.move_ip(deltaH, dir*y)

    def __storePreviousPosition(self):
        self.prevX = self.rect.x
        self.prevY = self.rect.y

    def __setDidMove(self):
        self.xChangedPositive = self.rect.x > self.prevX
        self.xChangedNegative = self.rect.x < self.prevX
        self.yChangedPositive = self.rect.y > self.prevY
        self.yChangedNegative = self.rect.y < self.prevY

    def __hasValidLeftInput(self):
        return (self.onFloor or self.onLadder) and self.playerKeysPressed[globals.PressedKeys.LEFT] and not self.playerKeysPressed[globals.PressedKeys.RIGHT]
    def __hasValidRightInput(self):
        return (self.onFloor or self.onLadder) and self.playerKeysPressed[globals.PressedKeys.RIGHT] and not self.playerKeysPressed[globals.PressedKeys.LEFT]
    def __hasValidUpInput(self):
        return self.onLadder and self.playerKeysPressed[globals.PressedKeys.UP] and not self.playerKeysPressed[globals.PressedKeys.DOWN]
    def __hasValidDownInput(self):
        return (self.onLadder or self.onRope) and self.playerKeysPressed[globals.PressedKeys.DOWN] and not self.playerKeysPressed[globals.PressedKeys.UP]

    def __checkQuadTreeCollisionsForDraw(self, root: quadtreenode.QuadTreeNode):
        if root is None: return
        root.quad.didCollide(self.rect)
        self.quadTreeCollisisionCalculated = self.quadTreeCollisisionCalculated + 1
        for child in root.children:
            self.__checkQuadTreeCollisionsForDraw(child)

    def __findSolidsInQuadTree(self, root: quadtreenode.QuadTreeNode, acc: List[collidable.Collidable], collidableIds: set[int]):
        if root is not None and root.quad.didCollide(self.rect):
            tmp = []
            for child in root.children:
                tmp = tmp + self.__findSolidsInQuadTree(child, acc, collidableIds)
            
            if root.children[0] is None:
                if len(root.collidables) > 0:
                    for solid in root.collidables:
                        solidId = id(solid)
                        if solidId not in collidableIds:
                            collidableIds.add(solidId)
                            tmp.append(solid)

            acc = acc+tmp
        return acc