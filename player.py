import pygame
import sys
import constants.globals as globals
import constants.colors as colors
import collidable
import quadtreenode
import playerstate.walkstate as walkstate
from pygame.locals import *
from typing import Optional
from typing import List

#TODO: Make this class "Player" a base class for Character (players, enemies, etc can be characters)
class Player(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, x: int, y: int, quadTree: quadtreenode.QuadTreeNode) -> None:
        super().__init__()
        self.surface = surface
        self.width = globals.PLAYER_W
        self.height = globals.PLAYER_H
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((colors.RED))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.keysPressed = [False,False,False,False]
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
        self.activeState = walkstate.WalkState()
        self.delta = 0
        self.deltaH = 0
        self.deltaY = 0
        self.gravity= 0
        self.quadTree = quadTree

    def changeState(self, newState):
        self.activeState.exit()
        self.activeState = newState
        newState.enter()

    def update(self, delta):
        self.delta = delta
        self.deltaH = delta * globals.H_SPEED
        self.deltaV = delta * globals.V_SPEED
        self.gravity = delta * globals.GRAVITY_SPEED
        self.__storePreviousPosition()
        newState = self.activeState.update(self)
        if newState is not None:
            self.changeState(newState)
        self.__setDidMove()
        if globals.DEBUG and self.didMove(): self.__checkQuadTreeCollisionsForDraw(self.quadTree)

    def drawPlayer(self):
        pygame.draw.rect(self.surface, colors.RED,  self.rect)

    
    # Not used at the moment, could use later though.
    def didMoveUp(self):
        return self.yChangedNegative
    def didMoveDown(self):
        return self.yChangedPositive
    def didMoveLeft(self):
        return self.xChangedNegative
    def didMoveRight(self):
        return self.xChangedPositive
    def didMove(self):
        return self.didMoveLeft() or self.didMoveRight() or self.didMoveUp() or self.didMoveDown()

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

    def handleMoveLeft(self):
        self.__handleMove(-self.deltaH, globals.ZERO, self.delta)
    def handleMoveRight(self):
        self.__handleMove(self.deltaH, globals.ZERO, self.delta)
    def handleMoveUp(self):
        self.__handleMove(globals.ZERO, -self.deltaV, self.delta)
    def handleMoveDown(self):
        self.__handleMove(globals.ZERO, self.deltaV, self.delta)
    def handleGravity(self):
        self.__handleMove(globals.ZERO, self.gravity, self.delta)

    def __handleMove(self, deltaH: float, deltaV: float, delta: float):
        willNotCollide = True
        collidables = self.__findSolidsInQuadTree(self.quadTree, [], set([]))
        # self.onLadder = False
        # self.onFloor = False
        self.touchingLadder = False
        for collidable in collidables:
            #self.collisionsCalculated = self.collisionsCalculated + 1
            if collidable.isSolid:
                if collidable.willCollide(self.rect, deltaH, deltaV):
                    self.onFloor = collidable.isFloor
                    if deltaH > 0: self.__resolveXGap(collidable, collidable.rect.left - self.rect.right, deltaV, 1)
                    if deltaH < 0: self.__resolveXGap(collidable, self.rect.left - collidable.rect.right, deltaV, -1)
                    if deltaV > 0: self.__resolveYGap(collidable, collidable.rect.top - self.rect.bottom, deltaH, 1)
                    if deltaV < 0: self.__resolveYGap(collidable, self.rect.top - collidable.rect.bottom, deltaH, -1)
                    willNotCollide = False
            elif collidable.didCollide(self.rect):
                if collidable.isLadder:
                    self.touchingLadder = True
            #     self.onFloor = False
                
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

    def __storePreviousPosition(self):
        self.prevX = self.rect.x
        self.prevY = self.rect.y

    def __setDidMove(self):
        self.xChangedPositive = self.rect.x > self.prevX
        self.xChangedNegative = self.rect.x < self.prevX
        self.yChangedPositive = self.rect.y > self.prevY
        self.yChangedNegative = self.rect.y < self.prevY

    def __checkQuadTreeCollisionsForDraw(self, root: quadtreenode.QuadTreeNode):
        if root is None: return
        root.quad.didCollide(self.rect)
        self.quadTreeCollisisionCalculated = self.quadTreeCollisisionCalculated + 1
        for child in root.children:
            self.__checkQuadTreeCollisionsForDraw(child)