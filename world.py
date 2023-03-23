import pygame, collidable, quadtreenode
import constants.globals as globals
import constants.colors as colors
from pygame.locals import *
from typing import List
from typing import Optional

class World():
    def __init__(self, surface: pygame.Surface) -> None:
        self.solidCollidableTileSet: List[collidable.Collidable] = []
        self.permeableCollidableTileSet: List[collidable.Collidable] = []
        self.rootQuadTreeNode = quadtreenode.QuadTreeNode(collidable.Collidable(0,0,globals.SCREEN_W,globals.SCREEN_H, False, colors.BLACK, colors.MAGENTA, True), self.getEmptyQuads(), [])
        self.surface = surface
        self.constructQuadTree(self.rootQuadTreeNode)
        self.initSolidTiles()

    def getQuadTree(self):
        return self.rootQuadTreeNode

    def initSolidTiles(self):
        for i in range(0,36):
            newTile = collidable.Collidable(i*32,704,32,32, True, colors.GREEN, colors.BLUE, isFloor=True)
            self.solidCollidableTileSet.append(newTile)
            self.insertCollidableIntoQuadTree(newTile, self.rootQuadTreeNode)

        for i in range(17,20):
            newTile = collidable.Collidable(i*32,290,32,32, True, colors.GREEN, colors.BLUE, isFloor=True)
            self.solidCollidableTileSet.append(newTile)
            self.insertCollidableIntoQuadTree(newTile, self.rootQuadTreeNode)

        for i in range(9,22):
            newTile = collidable.Collidable(500,i*32,32,32, False, colors.GRAY, colors.WHITE, isLadder=True)
            self.solidCollidableTileSet.append(newTile)
            self.insertCollidableIntoQuadTree(newTile, self.rootQuadTreeNode)
        
    def insertCollidableIntoQuadTree(self, collidable: collidable.Collidable, root: quadtreenode.QuadTreeNode):
        if root is None: return
        for child in root.children:
            if child is not None:
                childRect: pygame.rect = child.quad.rect
                if(collidable.didCollide(childRect)): self.insertCollidableIntoQuadTree(collidable, child)
        if root.children[0] is None:
            root.collidables.append(collidable)

    #TODO: Recursive version of this.
    def constructQuadTree(self, root: quadtreenode.QuadTreeNode):
        self.insertSubQuadsIntoQuad(self.rootQuadTreeNode)
        for subquad in self.rootQuadTreeNode.children:
            self.insertSubQuadsIntoQuad(subquad)
            for subsubquad in subquad.children:
                self.insertSubQuadsIntoQuad(subsubquad)
                for subsubsubquad in subsubquad.children:
                    self.insertSubQuadsIntoQuad(subsubsubquad)
                    for subsubsubsubquad in subsubsubquad.children:
                        self.insertSubQuadsIntoQuad(subsubsubsubquad)

    def insertSubQuadsIntoQuad(self, root: quadtreenode.QuadTreeNode):
        quadList = self.createSubQuads(root)
        root.children[globals.Quadrant.TOPLEFT] = quadList[globals.Quadrant.TOPLEFT]
        root.children[globals.Quadrant.TOPRIGHT] = quadList[globals.Quadrant.TOPRIGHT]
        root.children[globals.Quadrant.BOTTOMLEFT] = quadList[globals.Quadrant.BOTTOMLEFT]
        root.children[globals.Quadrant.BOTTOMRIGHT] = quadList[globals.Quadrant.BOTTOMRIGHT]
    
    # Given a root quad, generate a list of 4 subquads
    def createSubQuads(self, root: quadtreenode.QuadTreeNode) -> List[quadtreenode.QuadTreeNode]:
        result: List[quadtreenode.QuadTreeNode] = []
        topLeft = quadtreenode.QuadTreeNode(collidable.Collidable(root.quad.rect.x, root.quad.rect.y, root.quad.rect.width/2, root.quad.rect.height/2, False, colors.BLACK, colors.GREEN, True), self.getEmptyQuads(), [])
        topRight = quadtreenode.QuadTreeNode(collidable.Collidable(root.quad.rect.centerx, root.quad.rect.y, root.quad.rect.width/2, root.quad.rect.height/2, False, colors.BLACK, colors.GREEN, True), self.getEmptyQuads(), [])
        bottomLeft = quadtreenode.QuadTreeNode(collidable.Collidable(root.quad.rect.x, root.quad.rect.centery, root.quad.rect.width/2, root.quad.rect.height/2, False, colors.BLACK, colors.GREEN, True), self.getEmptyQuads(), [])
        bottomRight = quadtreenode.QuadTreeNode(collidable.Collidable(root.quad.rect.centerx, root.quad.rect.centery, root.quad.rect.width/2, root.quad.rect.height/2, False, colors.BLACK, colors.GREEN, True), self.getEmptyQuads(), [])
        return [topLeft, topRight, bottomLeft, bottomRight]
    
    def getEmptyQuads(self):
        return [None,None,None,None]
    
    def renderQuadTree(self):
        self.__renderQuadTree(self.rootQuadTreeNode)
    
    def __renderQuadTree(self, root: Optional[quadtreenode.QuadTreeNode]):
        #base case
        if root is None:
            return

        for child in root.children:
            self.__renderQuadTree(child)
        
        root.quad.draw(self.surface)

    def renderTileSet(self):
        for solidTile in self.solidCollidableTileSet:
            solidTile.draw(self.surface)
        for permeableTile in self.permeableCollidableTileSet:
            permeableTile.draw(self.surface)