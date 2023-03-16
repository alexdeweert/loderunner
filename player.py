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
        
    def drawPlayer(self, screen: pygame.Surface):
        pygame.draw.rect(screen, colors.RED,  self.rect)

    def updatePlayerPosition(self,delta,hSpeed,vSpeed):
        resolvedHSpeed = delta * hSpeed
        resolvedVSpeed = delta * vSpeed
        if(self.playerKeysPressed[globals.PressedKeys.LEFT]): self.rect.move_ip(-resolvedHSpeed, globals.ZERO)
        if(self.playerKeysPressed[globals.PressedKeys.RIGHT]): self.rect.move_ip(resolvedHSpeed, globals.ZERO)
        if(self.playerKeysPressed[globals.PressedKeys.UP]): self.rect.move_ip(globals.ZERO, -resolvedVSpeed)
        if(self.playerKeysPressed[globals.PressedKeys.DOWN]): self.rect.move_ip(globals.ZERO, resolvedVSpeed)

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
    def resolveCollisionWith(self, rect: pygame.Rect) -> Optional[pygame.Rect]:
        """
        TODO: How can we resolve this?
        Yes, we know a collision occured - but we can't set the player's x or y unless we know
        where to restrict it. But we CAN test again, if its not left of, not right of, etc - and whichever
        of those fails we can update the x or y depending - its possible that two conditions can be false
        at the same time, so we need to resolve all the collisions.
        """
        # We know a collision occured - so resolve the players position
        if(rect is not None):
            # If player not right of, then its inside of the rect
            isLeftOf = self.rect.right < rect.left
            isRightOf = self.rect.left > rect.right
            isBelow = self.rect.top > rect.bottom
            isAbove = self.rect.bottom < rect.top

            if(not isLeftOf and self.rect.left < rect.left):
                self.rect.right = rect.left
            if(not isRightOf and self.rect.right > rect.right):
                self.rect.left = rect.right

            # TODO: Above works without below - need to figure this out
            # Might be a good idea to draw it out.
            
            # if(not isBelow and self.rect.bottom > rect.bottom):
            #     self.rect.top = rect.bottom
            # if(not isAbove and self.rect.top < rect.top):
            #     self.rect.bottom = rect.top