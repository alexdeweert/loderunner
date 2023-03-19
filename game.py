import pygame, sys, player, collidable, quadtreenode
import constants.globals as globals
import constants.colors as colors
from pygame.locals import *
from enum import IntEnum
from typing import List

class Game():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.player = player.Player()
        # We can disable rendering of the root quad eventually (once we have the quad tree working)
        self.solidCollidableTileSet: List[collidable.Collidable] = list()
        self.permeableCollidableTileSet: List[collidable.Collidable] = list()

        width = 0
        while(width <= (globals.SCREEN_W - 32)):
            self.solidCollidableTileSet.append(collidable.Collidable(width,700,32,16, True, colors.GREEN, colors.BLUE))
            width += 32
        self.permeableCollidableTileSet.append(collidable.Collidable(10,50,163,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(84,125,80,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(148,175,163,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(300,125,163,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(394,40,100,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(560,145,163,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(650,64,75,32, False, colors.WHITE, colors.GRAY))
        self.permeableCollidableTileSet.append(collidable.Collidable(780,150,180,32, False, colors.WHITE, colors.GRAY))

        pygame.display.set_caption(globals.SCREEN_CAPTION)
        self.surface = pygame.display.set_mode((globals.SCREEN_W, globals.SCREEN_H))

        # For now we need to check collisions with all quadtreenodes so we can render them properly.
        # Wherever something is on the screen (player etc) it WILL be in a quad leaf node.

        # How can the moving object be determined to colliding with a quad if its not in the child list?
        # A given object is always in a leaf node. So we should always take the player's location, search the tree,
        # and get the items from the leaf nodes that it's touching.

        #The player itself maybe doesn't have to be entered in the tree - the only things that need to query the tree
        #passing in its own position (to search) are items that need to know about all the other items.

        #For moving enemies we do need to update their position in the tree.
        #But how can we do that efficiently?

        #For now we DO need just construct the tree, and then add static objects there.
        #But eventually yes, we need to determine the optimal way of updating moving objects (player, enemies) in the tree.
        #Can we recursively construct the quadtree?
        self.rootQuad = collidable.Collidable(0,0,globals.SCREEN_W,globals.SCREEN_H, False, colors.BLACK, (255,255,255), True)
        self.rootQuadTreeNode = quadtreenode.QuadTreeNode(self.rootQuad, 0, 0)
        # for i in range(globals.QUAD_TREE_DEPTH):
            # add 4 children per level, 
    
    # def constructQuadTree(self, root: quadtreenode.QuadTreeNode, level: int):
    #     #If we reached the bottom level, add the empty list and just return a constructed leaf node.
    #     if level == globals.QUAD_TREE_DEPTH:
    #         #make the collidable some division of the level depending on the width of the screen etc
    #         #also need the parent so we know how to define this new node quad's x and y.
    #         #the node also needs to know if its a 1st, 2nd, 3rd, or 4th child so it can property set its dimensions.
    #         return root
        
    #     #At this level we make it
    #     newNode = quadtreenode.QuadTreeNode()


    def renderFpsText(self):
        fpsString = f"fps: {str(int(self.clock.get_fps()))}"
        renderedFpsText = globals.DEBUG_FONT.render(fpsString, True, globals.DEBUG_FONT_COLOR)
        
        return renderedFpsText
    
    def renderCollisionsText(self):
        bruteForceCollisions = f"collisions: {str(self.player.collisionsCalculated)}"
        renderedBruteForceCollisions = globals.COLLISIONS_FONT.render(bruteForceCollisions, True, globals.DEBUG_FONT_COLOR)
        return renderedBruteForceCollisions


    # React to events (input, etc)
    def processInput(self):
        for event in pygame.event.get():
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYDOWN)
            self.player.processMovementWithKeyEventTypes(event, pygame.KEYUP)
            self.player.processQuitGameConditions(event)

    # Update game logic based on inputs
    def update(self, delta):
        '''
        TODO: We want to add and remove collidable tiles (and permeable tiles) only if they're in the same quadrant as the player
        otherwise they should be removed from the list to check.
        
        There should be a single quad tree, and as the player moves it's position within the tree will be updated.
        
        All static items during initial population (and during dynamic creation/destruction during gamerplay) will be
        added to the quad tree.

        The player itself (or npc players, enemies) can query the tree to determine which list (at a leaf node) to check collisions against.
        
        In a normal binary tree we can traverse by comparing the current value to the node, and knowing if its less (go left) or equal (go right).
        In this case, a value is a co-ordinate pair. Lets consider the simplest case (the tree is only one level deep, ie; 4 quadrants).

        If we wanted to add the player to a quadrant, how can we determine where to go? The parent node is the entire screen.
        If there were zero levels all elements would be in this list, since they're all in the same quadrant.

        At the first level, we have 4 nodes. Consider thet top left node (top left of 4 quadrants).
        It's essentially a box with x, y, width, height. Can we represent this object as a pygame rect? Maybe that's too heavy.
        Although, the pygame.rect does make things like left and right, top and bottom to work with.

        We need to determine how to construct a quad tree N levels deep.
        Could we do it recursively? ie; base case is: if level == N, don't add any more quads, just return the list at that level.
        How do we represent each node? Each node has: a quad (a collidable), children (other collidable rects).
        
        If a quadTreeNode has None children, then its a leaf node. Itself is a quad, yes - but what we're interested in is the case
        when its Children is empty (because then its a leafnode) - in that case, we return its optional collidables list.

        Node(Quad, List[Quad], )

        At that level, 
        '''
        self.player.updatePlayerPosition(delta, globals.H_SPEED, globals.V_SPEED, self.solidCollidableTileSet, self.permeableCollidableTileSet, self.rootQuad)

    # Render drawable objects
    def render(self):
        self.surface.fill(colors.BLACK)
        self.surface.blit(self.renderFpsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y))
        self.surface.blit(self.renderCollisionsText(), (globals.FPS_DISP_X, globals.FPS_DISP_Y + 16))
        self.rootQuad.draw(self.surface)
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