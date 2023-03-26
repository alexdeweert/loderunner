import pygame
import interfaces.basestate as basestate
import playerstate.climbstate as climbstate
import collidable
import quadtreenode
import constants.globals as globals
from typing import List

class WalkState(basestate.BaseState):
    def __init__(self) -> None:
        super().__init__()

    def enter(self):
        print("WalkState enter")
    
    def exit(self):
        print("WalkState exit")

    #TODO: change player.Player to character.Character once we make character an inheritable class for any movable entity
    def update(self, character):
        if self.__hasValidLeftInput(character): character.handleMoveLeft()
        if self.__hasValidRightInput(character): character.handleMoveRight()
        if self.__hasValidUpInput(character): return climbstate.ClimbState()
        #TODO: Move this into the falling state
        character.handleGravity()
    
    def __hasValidLeftInput(self, character):
        return character.keysPressed[globals.PressedKeys.LEFT] and not character.keysPressed[globals.PressedKeys.RIGHT]
    def __hasValidRightInput(self, character):
        return character.keysPressed[globals.PressedKeys.RIGHT] and not character.keysPressed[globals.PressedKeys.LEFT]
    def __hasValidUpInput(self, character):
        return character.touchingLadder and character.keysPressed[globals.PressedKeys.UP] and not character.keysPressed[globals.PressedKeys.DOWN]

    def input(self, event: pygame.event.Event):
        print("walkstate input)")