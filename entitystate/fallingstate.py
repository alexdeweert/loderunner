import pygame
import interfaces.ibasestate as ibasestate
import constants.globals as globals
import entitystate.walkstate as walkstate
import entitystate.climbstate as climbstate
from typing import List

class FallingState(ibasestate.IBaseState):
    def __init__(self, entity) -> None:
        super().__init__()
        self.entity = entity

    def enter(self):
        print("FallingState enter")
    
    def exit(self):
        print("FallingState exit")

    def update(self):
        self.entity.handleGravity(isFalling = True)
        if self.entity.onFloor: return walkstate.WalkState(self.entity)
        if self.entity.touchingLadder:
            return climbstate.ClimbState(self.entity)

    def input(self, event: pygame.event.Event):
        print("walkstate input)")