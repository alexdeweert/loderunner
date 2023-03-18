import pygame
import sys
import constants.globals as globals
import constants.colors as colors
from typing import Optional

class Collidable():
    def __init__(self, x, y, width, height) -> None:
        self.rect: pygame.Rect = pygame.Rect(x,y,width,height)
        self.rectColor = colors.GREEN
    
    def getX(self) -> int:
        return self.rect.x
    
    def getY(self) -> int:
        return self.rect.y
    
    def didCollide(self, withRect: pygame.Rect) -> Optional[pygame.Rect]:
        isLeftOf = self.rect.right < withRect.left
        isRightOf = self.rect.left > withRect.right
        isBelow = self.rect.top > withRect.bottom
        isAbove = self.rect.bottom < withRect.top
        didCollide = not(isLeftOf or isRightOf or isBelow or isAbove)
        self.rectColor = colors.BLUE if didCollide else colors.GREEN
        if(didCollide):
            return self.rect
        return None
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.rectColor,  self.rect)