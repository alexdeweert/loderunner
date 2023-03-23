import pygame
import constants.globals as globals
import constants.colors as colors
from typing import Optional

class Collidable():
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            isSolid: Optional[bool],
            color: Optional[pygame.Color],
            touchedColor: Optional[pygame.Color],
            isQuad: bool = False,
            isFloor: bool = False,
            isLadder: bool = False
        ) -> None:
        
        self.rect: pygame.Rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.touchedColor = touchedColor
        self.isSolid = isSolid
        self.touched = False
        self.isQuad = isQuad
        self.isFloor = isFloor
        self.isLadder = isLadder
    
    # Use for detecting collisions where we allow overlapping
    def didCollide(self, withRect: pygame.Rect) -> bool:
        didCollide = self.__isCollision(globals.ZERO, globals.ZERO, withRect)
        self.touched = didCollide
        return didCollide
    
    # Use for detecting if a proposed movement will result in a collision.
    # We check this to determine if we will allow continued movement in a direction.
    def willCollide(self, withRect: pygame.Rect, proposedX: float, proposedY: float) -> Optional[pygame.Rect]:
        willCollide = self.__isCollision(proposedX, proposedY, withRect)
        self.touched = willCollide
        return willCollide
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (self.touchedColor if self.touched else self.color),  self.rect, 1 if self.isQuad else 0)

    def __isCollision(self, withModX, withModY, withRect: pygame.Rect):
        isLeftOf = self.rect.right < withRect.left+withModX
        isRightOf = self.rect.left > withRect.right+withModX
        isBelow = self.rect.top > withRect.bottom+withModY
        isAbove = self.rect.bottom < withRect.top+withModY
        return not(isLeftOf or isRightOf or isBelow or isAbove)