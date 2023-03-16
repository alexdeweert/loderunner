import pygame
import sys
import constants.globals as globals
import constants.colors as colors

class Collidable():
    def __init__(self, x, y, width, height) -> None:
        self.rect: pygame.Rect = pygame.Rect(x,y,width,height)
        self.rectColor: colors.GREEN
    
    def getX(self) -> int:
        return self.rect.x
    
    def getY(self) -> int:
        return self.rect.y
    
    def didCollide(self, withRect: pygame.Rect) -> bool:
        #right < left
        isLeftOf = self.rect.right < withRect.left
        #left > right
        isRightOf = self.rect.left > withRect.right
        #top > bottom
        isBelow = self.rect.top > withRect.bottom
        #bottom < top
        isAbove = self.rect.bottom < withRect.top

        didCollide = not(isLeftOf or isRightOf or isBelow or isAbove)
        self.rectColor = colors.RED if didCollide else colors.GREEN

        return not(isLeftOf or isRightOf or isBelow or isAbove)
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.rectColor,  self.rect)