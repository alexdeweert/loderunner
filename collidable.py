import pygame
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
        didCollide = self.isCollision(globals.ZERO, globals.ZERO, withRect)
        self.touched = didCollide
        return didCollide
    
    # Use for detecting if a proposed movement will result in a collision.
    # We check this to determine if we will allow continued movement in a direction.
    # As noted in the player fn which calls this, this solution does not solve tunnelling. 
    def willCollide(self, withRect: pygame.Rect, proposedX: float, proposedY: float) -> Optional[pygame.Rect]:
        willCollide = self.isCollision(proposedX, proposedY, withRect)
        self.touched = willCollide
        return willCollide
    
    def isCollision(self, withModX, withModY, withRect: pygame.Rect):
        isLeftOf = self.rect.right < withRect.left+withModX
        isRightOf = self.rect.left > withRect.right+withModX
        isBelow = self.rect.top > withRect.bottom+withModY
        isAbove = self.rect.bottom < withRect.top+withModY
        return not(isLeftOf or isRightOf or isBelow or isAbove)

    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (self.touchedColor if self.touched else self.color),  self.rect, 1 if self.isQuad else 0)