import pygame
import collidable
from typing import List
from typing import Optional

class QuadTreeNode():
    def __init__(self, quad: collidable.Collidable, level: int, siblingDesignation: int, children: Optional[List] = None, collidables: Optional[collidable.Collidable] = None) -> None:
        self.quad = quad
        self.children = children
        self.level = level
        self.collidables = collidables
        self.siblingDesignation = siblingDesignation