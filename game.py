import pygame, sys, player, collidable, quadtreenode
import constants.globals as globals
import constants.colors as colors
from pygame.locals import *
from enum import IntEnum
from typing import List
from typing import Optional

class Game():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.player = player.Player()
        # We can disable rendering of the root quad eventually (once we have the quad tree working)
        self.solidCollidableTileSet: List[collidable.Collidable] = list()
        self.permeableCollidableTileSet: List[collidable.Collidable] = list()
        self.children = 0

        pygame.display.set_caption(globals.SCREEN_CAPTION)
        self.surface = pygame.display.set_mode((globals.SCREEN_W, globals.SCREEN_H))
        self.rootQuadTreeNode = quadtreenode.QuadTreeNode(collidable.Collidable(0,0,globals.SCREEN_W,globals.SCREEN_H, False, colors.BLACK, colors.MAGENTA, True), self.getEmptyQuads(), list())
        self.constructQuadTree(self.rootQuadTreeNode)

        # QUADTREE tiles
        #self.quadtreeTile = collidable.Collidable(2,2,16,16, True, colors.GREEN, colors.BLUE)
        self.quadtreeTile2 = collidable.Collidable(208,88,16,16, True, colors.GREEN, colors.BLUE)
        # Add tiles to QUADTREE
        #self.insertCollidableIntoQuadTree(self.quadtreeTile, self.rootQuadTreeNode)
        self.insertCollidableIntoQuadTree(self.quadtreeTile2, self.rootQuadTreeNode)
        

    # Where can a tile exist within a quadtreenode, only the bottom level?
    # Consider the case where the tile is in the exact middle of the screen.
    # It touches the root node, 4 corners of the its subnodes, all the way down.
    # So we need to actually reference an inserted tile in MORE THAN JUST ONE node.
    # It can exist in many nodes (regardless of parent, child, etc designation if any).
    # So when we insert, we almost need to recurse down ONLY when there is a collision.
    # We return IF: its None, yes of course, but if there's no collision, we can also return.
    # We only need to go down if there's an actual collision with that node.
    def insertCollidableIntoQuadTree(self, collidable: collidable.Collidable, root: quadtreenode.QuadTreeNode):
        if root is None: return

        #Okay so the rule should be, only add to the collidables list IF its a child node (ie; there are no children below it)
        #And we recur down ONLY if a collision exists - there's no point in recurring down if theres no collision with a child.
        #So why is this more efficient (its an extension of broad phase)
        #If there are 4 levels, there are only AT MOST 4^4 (256 checks) traversals downward
        #4^5 checks (5 levels) is 1024 checks

        #root.children needs to actually have children (ie; it cant be none type)
        for child in root.children:
            if child is not None:
                childRect: pygame.rect = child.quad.rect
                if(collidable.didCollide(childRect)): self.insertCollidableIntoQuadTree(collidable, child)
        
        #If we got here then there was a collision with the collidable up until this point.
        #If that's true then we add the collidable to this nodes list of collidables.]
        if root.children[0] is None:
            print(f"INSERTED collidable at x: {collidable.rect.x}, y: {collidable.rect.y}")
            root.collidables.append(collidable)



    # A programmatic way of constructing a quadtree of 4 levels
    # TODO: A recursive function that constructs N levels of quadtrees (for more fine grained control)
    def constructQuadTree(self, root: quadtreenode.QuadTreeNode):
        self.insertSubQuadsIntoQuad(self.rootQuadTreeNode)
        for subquad in self.rootQuadTreeNode.children:
            self.insertSubQuadsIntoQuad(subquad)
            for subsubquad in subquad.children:
                self.insertSubQuadsIntoQuad(subsubquad)
                # for subsubsubquad in subsubquad.children:
                #     self.insertSubQuadsIntoQuad(subsubsubquad)
        print(f"Children: {self.children}")

    def insertSubQuadsIntoQuad(self, root: quadtreenode.QuadTreeNode):
        quadList = self.createSubQuads(root)
        root.children[globals.Quadrant.TOPLEFT] = quadList[globals.Quadrant.TOPLEFT]
        root.children[globals.Quadrant.TOPRIGHT] = quadList[globals.Quadrant.TOPRIGHT]
        root.children[globals.Quadrant.BOTTOMLEFT] = quadList[globals.Quadrant.BOTTOMLEFT]
        root.children[globals.Quadrant.BOTTOMRIGHT] = quadList[globals.Quadrant.BOTTOMRIGHT]
        self.children = self.children + 4
    
    # Given a root quad, generate a list of 4 subquads
    def createSubQuads(self, root: quadtreenode.QuadTreeNode) -> List[quadtreenode.QuadTreeNode]:
        result: List[quadtreenode.QuadTreeNode] = list()
        topLeft = quadtreenode.QuadTreeNode(collidable.Collidable(root.quad.rect.x, root.quad.rect.y, root.quad.rect.width/2, root.quad.rect.height/2, False, colors.BLACK, colors.GREEN, True), self.getEmptyQuads(), list())
        topRight = quadtreenode.QuadTreeNode(collidable.Collidable(root.quad.rect.centerx, root.quad.rect.y, root.quad.rect.width/2, root.quad.rect.height/2, False, colors.BLACK, colors.GREEN, True), self.getEmptyQuads(), list())
        bottomLeft = quadtreenode.QuadTreeNode(collidable.Collidable(root.quad.rect.x, root.quad.rect.centery, root.quad.rect.width/2, root.quad.rect.height/2, False, colors.BLACK, colors.GREEN, True), self.getEmptyQuads(), list())
        bottomRight = quadtreenode.QuadTreeNode(collidable.Collidable(root.quad.rect.centerx, root.quad.rect.centery, root.quad.rect.width/2, root.quad.rect.height/2, False, colors.BLACK, colors.GREEN, True), self.getEmptyQuads(), list())
        return [topLeft, topRight, bottomLeft, bottomRight]
    
    def getEmptyQuads(self):
        return [None,None,None,None]
    
    #The children of a quad tree can be either [node, node, node, node] or [None...]
    #since the children can point to a None object, the recursive algorithm can check the base case to see if its None
    #The root param itself can be None - so this seems necessary
    def renderQuadTree(self, root: Optional[quadtreenode.QuadTreeNode]):
        #base case
        if root is None:
            return

        #in this case the root is an actual quadtreenode - so render itself, then drill into children
        #order shouldn't matter
        for child in root.children:
            self.renderQuadTree(child)
        
        root.quad.draw(self.surface)

    def renderFpsText(self):
        fpsString = f"fps: {str(int(self.clock.get_fps()))}"
        renderedFpsText = globals.DEBUG_FONT.render(fpsString, True, globals.DEBUG_FONT_COLOR)
        
        return renderedFpsText
    
    def renderCollisionsText(self):
        bruteForceCollisions = f"collisions: {str(self.player.collisionsCalculated)}"
        renderedBruteForceCollisions = globals.DEBUG_FONT.render(bruteForceCollisions, True, globals.DEBUG_FONT_COLOR)
        return renderedBruteForceCollisions
    
    def renderPlayerPosition(self):
        playerPosition = f"PlayerX: {str(self.player.rect.x)}, PlayerY: {str(self.player.rect.y)}"
        return globals.DEBUG_FONT.render(playerPosition, True, globals.DEBUG_FONT_COLOR)


    # React to events (input, etc)
    def processInput(self):
        for event in pygame.event.get():
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYDOWN)
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYUP)
            self.player.processQuitGameConditions(event)

    # Update game logic based on inputs
    def update(self, delta):
        self.player.updatePlayerPosition(delta, globals.H_SPEED, globals.V_SPEED, self.rootQuadTreeNode)

    # Render drawable objects
    def render(self):
        self.surface.fill(colors.BLACK)

        #Need to recursively render the quads in the rootQuadTree
        self.renderQuadTree(self.rootQuadTreeNode)

        self.surface.blit(self.renderFpsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y))
        self.surface.blit(self.renderCollisionsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y + 16))
        self.surface.blit(self.renderPlayerPosition(), (globals.FPS_DISP_X, globals.FPS_DISP_Y + 32))
        #self.quadtreeTile.draw(self.surface)
        self.quadtreeTile2.draw(self.surface)
        self.player.drawPlayer(self.surface)
        # TODO: move tilesets logic to world class
        for solidTile in self.solidCollidableTileSet:
            solidTile.draw(self.surface)
        for permeableTile in self.permeableCollidableTileSet:
            permeableTile.draw(self.surface)
        pygame.display.flip()
        
    def run(self):
        while True:
            delta = self.clock.tick(globals.FPS) / globals.SECOND_MS
            pygame.time.delay(globals.SIMULATED_LAG_MS)
            if(delta > globals.MAX_DELTA):
                delta = globals.MAX_DELTA
            self.processInput()
            self.update(delta)
            self.render()

if __name__ == '__main__':
    pygame.init()
    globals.init()
    colors.init()
    Game().run()