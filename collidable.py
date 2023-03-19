import pygame
import sys
import constants.globals as globals
import constants.colors as colors
from typing import Optional

class Collidable():
    def __init__(self, x: int, y: int, width: int, height: int, solid: Optional[bool], color: Optional[pygame.Color], touchedColor: Optional[pygame.Color], isQuad: bool = False) -> None:
        self.rect: pygame.Rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.touchedColor = touchedColor
        self.solid = solid
        self.touched = False
        self.isQuad = isQuad
    
    # Use for detecting collisions where we allow overlapping
    def didCollide(self, withRect: pygame.Rect) -> bool:
        isLeftOf = self.rect.right < withRect.left
        isRightOf = self.rect.left > withRect.right
        isBelow = self.rect.top > withRect.bottom
        isAbove = self.rect.bottom < withRect.top
        didCollide = not(isLeftOf or isRightOf or isBelow or isAbove)
        self.touched = didCollide
        return didCollide
    
    # Use for detecting if a proposed movement will result in a collision.
    # We check this to determine if we will allow continued movement in a direction.
    # As noted in the player fn which calls this, this solution does not solve tunnelling. 
    def willCollide(self, withRect: pygame.Rect, proposedX: float, proposedY: float) -> Optional[pygame.Rect]:
        isLeftOf = self.rect.right < withRect.left+proposedX
        isRightOf = self.rect.left > withRect.right+proposedX
        isBelow = self.rect.top > withRect.bottom+proposedY
        isAbove = self.rect.bottom < withRect.top+proposedY
        willCollide = not(isLeftOf or isRightOf or isBelow or isAbove)
        self.touched = willCollide
        return willCollide
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (self.touchedColor if self.touched else self.color),  self.rect, 1 if self.isQuad else 0)