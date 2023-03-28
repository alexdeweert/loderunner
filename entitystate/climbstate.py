import pygame
import interfaces.ibasestate as ibasestate
import constants.globals as globals
import entitystate.fallingstate as fallingstate
from typing import List

class ClimbState(ibasestate.IBaseState):
    def __init__(self, entity) -> None:
        super().__init__()
        self.entity = entity

    def enter(self):
        print("ClimbState enter")

    
    def exit(self):
        print("ClimbState exit")

    def update(self):

        #In the case when they're touching floor (TODO: should be a wall solid collidable if we want slide behavior)
        #AND there's a diagonal movement, do up or down instead of horizontal

        #Prioritize resolving diagonal input as horizontal
        inputDiagonalLeft = self.__hasValidDiagonalLeft()
        inputDiagonalRight = self.__hasValidDiagonalRight()
        # inputDiagonalUpLeft = self.__hasDiagonalUpLeft()
        # inputDiagonalUpRight = self.__hasDiagonalUpRight()
        # if self.entity.onFloor and (inputDiagonalUpLeft or inputDiagonalUpRight):
        #     if inputDiagonalUpLeft: self.entity.handleMoveUp()
        #     if inputDiagonalUpRight: self.entity.handleMoveRight()
        if not self.entity.onFloor and (inputDiagonalLeft or inputDiagonalRight):
            if inputDiagonalLeft: self.entity.handleMoveLeft()
            if inputDiagonalRight: self.entity.handleMoveRight()
        else:
            if self.__hasValidUpInput(): self.entity.handleMoveUpLadder()
            if self.__hasValidDownInput(): self.entity.handleMoveDownLadder()
            if self.__hasValidLeftInput(): self.entity.handleMoveLeft()
            if self.__hasValidRightInput(): self.entity.handleMoveRight()

        if not self.entity.onFloor and not self.entity.touchingLadder and not self.entity.onRope:
            return fallingstate.FallingState(self.entity)
    def __hasDiagonalUpLeft(self):
        return self.__hasValidLeftInput() and self.__hasValidUpInput()
    def __hasDiagonalUpRight(self):
        return self.__hasValidRightInput() and self.__hasValidUpInput()
    def __hasValidDiagonalLeft(self):
        return self.__hasValidLeftInput() and (self.__hasValidDownInput() or self.__hasValidUpInput())
    def __hasValidDiagonalRight(self):
        return self.__hasValidRightInput() and (self.__hasValidDownInput() or self.__hasValidUpInput())
    def __hasValidUpInput(self):
        return self.entity.keysPressed[globals.PressedKeys.UP] and not self.entity.keysPressed[globals.PressedKeys.DOWN]
    def __hasValidDownInput(self):
        return self.entity.keysPressed[globals.PressedKeys.DOWN] and not self.entity.keysPressed[globals.PressedKeys.UP]
    def __hasValidLeftInput(self):
        return self.entity.keysPressed[globals.PressedKeys.LEFT] and not self.entity.keysPressed[globals.PressedKeys.RIGHT]
    def __hasValidRightInput(self):
        return self.entity.keysPressed[globals.PressedKeys.RIGHT] and not self.entity.keysPressed[globals.PressedKeys.LEFT]

    def input(self, event: pygame.event.Event):
        print("walkstate input)")