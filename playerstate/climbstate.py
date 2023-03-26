import pygame
import interfaces.basestate as basestate
import collidable
import quadtreenode
import constants.globals as globals
from typing import List

class ClimbState(basestate.BaseState):
    def __init__(self) -> None:
        super().__init__()

    def enter(self):
        print("ClimbState enter")
    
    def exit(self):
        print("ClimbState exit")

    def update(self, character):
        if self.__hasValidUpInput(character): character.handleMoveUp()
        if self.__hasValidDownInput(character): character.handleMoveDown()

    def __hasValidUpInput(self, character):
        return character.keysPressed[globals.PressedKeys.UP] and not character.keysPressed[globals.PressedKeys.DOWN]
    
    def __hasValidDownInput(self, character):
        return character.keysPressed[globals.PressedKeys.DOWN] and not character.keysPressed[globals.PressedKeys.UP]

    def input(self, event: pygame.event.Event):
        print("walkstate input)")