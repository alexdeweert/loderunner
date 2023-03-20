import pygame
import collidable
from typing import List
from typing import Optional

class QuadTreeNode():
    def __init__(self, quad: collidable.Collidable, children: List, collidables: List[collidable.Collidable]) -> None:
        self.quad = quad
        # Children are other quadtree nodes
        self.children = children
        self.collidables = collidables