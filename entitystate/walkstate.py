import pygame
import interfaces.ibasestate as ibasestate
import entitystate.climbstate as climbstate
import entitystate.fallingstate as fallingstate
import collidable
import quadtreenode
import constants.globals as globals
from typing import List

class WalkState(ibasestate.IBaseState):
    def __init__(self, entity) -> None:
        super().__init__()
        self.entity = entity

    def enter(self):
        print("WalkState enter")
    
    def exit(self):
        print("WalkState exit")
        
    def update(self):
        if not self.entity.onFloor and not self.entity.touchingLadder and not self.entity.onRope:
            return fallingstate.FallingState(self.entity)
        if self.__hasValidUpInput() or self.__hasValidDownInput():
            return climbstate.ClimbState(self.entity)
        if self.__hasValidLeftInput(): self.entity.handleMoveLeft()
        if self.__hasValidRightInput(): self.entity.handleMoveRight()
        if not self.entity.touchingLadder:
            self.entity.handleGravity()
    
    def __hasValidLeftInput(self):
        return self.entity.keysPressed[globals.PressedKeys.LEFT] and not self.entity.keysPressed[globals.PressedKeys.RIGHT]
    def __hasValidRightInput(self):
        return self.entity.keysPressed[globals.PressedKeys.RIGHT] and not self.entity.keysPressed[globals.PressedKeys.LEFT]
    def __hasValidUpInput(self):
        return self.entity.touchingLadder and self.entity.keysPressed[globals.PressedKeys.UP] and not self.entity.keysPressed[globals.PressedKeys.DOWN] and not self.__hasValidLeftInput() and not self.__hasValidRightInput()
    def __hasValidDownInput(self):
        return self.entity.touchingLadder and self.entity.keysPressed[globals.PressedKeys.DOWN] and not self.entity.keysPressed[globals.PressedKeys.UP] and not self.__hasValidLeftInput() and not self.__hasValidRightInput()
    def __hasValidDiagonalLeft(self):
        return self.__hasValidLeftInput() and (self.__hasValidUpInput())
    def __hasValidDiagonalRight(self):
        return self.__hasValidRightInput() and (self.__hasValidUpInput())

    def input(self, event: pygame.event.Event):
        print("walkstate input)")