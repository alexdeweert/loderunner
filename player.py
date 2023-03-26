import pygame
import quadtreenode
import entity
from pygame.locals import *
from typing import List

class Player(entity.Entity):
    def __init__(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, quadTree: quadtreenode.QuadTreeNode) -> None:
        super(Player, self).__init__(surface, x, y, width, height, quadTree)