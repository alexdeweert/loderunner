import pygame
import sys
import constants.globals as globals
import constants.colors as colors
import collidable
import quadtreenode
from pygame.locals import *
from typing import Optional
from typing import List

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = globals.PLAYER_W
        self.height = globals.PLAYER_H
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((colors.RED))
        self.rect = self.image.get_rect()
        # self.rect.x = 500
        # self.rect.y = 500
        self.playerKeysPressed = [False,False,False,False]
        self.prevX = self.rect.x
        self.prevY = self.rect.y
        self.xChangedPositive = False
        self.xChangedNegative = False
        self.yChangedPositive = False
        self.yChangedNegative = False
        self.collisionsCalculated = 0
        self.quadTreeCollisisionCalculated = 0
        
    def drawPlayer(self, screen: pygame.Surface):
        pygame.draw.rect(screen, colors.RED,  self.rect)

    #TODO: Maybe make a Vector2 class (with an x and magnitude)
    def updatePlayerPosition(self, delta, hSpeed, vSpeed, quadTree: quadtreenode.QuadTreeNode):
        deltaH = delta * hSpeed
        deltaV = delta * vSpeed
        self.storePreviousPosition()
        if self.hasValidLeftInput(): self.handleMove(-deltaH, globals.ZERO, quadTree)
        if self.hasValidRightInput(): self.handleMove(deltaH, globals.ZERO, quadTree)
        if self.hasValidUpInput(): self.handleMove(globals.ZERO, -deltaV, quadTree)
        if self.hasValidDownInput(): self.handleMove(globals.ZERO, deltaV, quadTree)
        self.setDidMove()

    def handleMove(self, deltaH: float, deltaV: float, quadTree: quadtreenode.QuadTreeNode):
        willNotCollide = True

        #Given the quadtree, based on the players location we search down, depending on whether a collision exists, until we get
        #To the bottom. So, at every step we are performing 4^n checks, s.t. n is the number of levels down. ie; at 5 levels we have 1024
        #checks in every frame - this is a lot when we don't have very many objects. But as the number of collidable objects grow, the number
        #of brute force checks go down. For example, if we have 5 objects all checking each other's position at every frame (when a single object
        # does 5 checks every frame, then we have 5*5 checks where they all check eachother). Assume have n^2 checks in a brute force situation.
        
        # Depending on screen dimensions, with 5 levels we get 1364 bottom level quads.
        # Assume we have 1364 objects, all brute force checking each other. This is over 1.8 million collision checks at every frame.
        # Assume that these same objects are inserted into a quad tree, all in a single spot. The player is not colliding with the quad that
        # holds that group of objects. However, if the player occupies that same quad, then yes, those 1.8 million checks will occur. This is
        # certainly a weakness of the quadtree method. But the chances of all objects appearing in a single spot - while stastically possible -
        # is very tiny (or just poor design).

        # Instead, imagine that those 1364 objects are spread evenly, one in each bottom level quad.
        # Then, at every frame, the player queries the quadtree, searching only the quad that it currently occupies, down to the bottom level.
        # And then it sees the list of collidables in that quadrant - then and only then does it do the more expensive collisision detection and
        # resolution.

        #So, if there are 5 levels of subquadrants, how many checks does the player do in order every frame to get the list of possible collidables?
        #log(4^5). And then the number of collisions (which, at its lowest level is the number of collidables, but in reality its the probability
        # that any number of collidables will exist in a given location.) Its upper bounded by log(4^k) * n^2 s.t. k is the number of levels of the
        # quad tree, and n is the number of collidable objects in the game, at every frame.

        staticSolids = self.findStaticCollidablesInQuadTree(quadTree, set([]), [])
        print(f"static: solids in this frame: {len(staticSolids)}")

        #The withSolids will be contained within a quadTree search.
        #We searchin within the quadtree, based on the player's location, and get back a list of solids here.
        #This is in contrast to passing in an entire list of solids (from game.py)
        #For the moment we just want to render the quads (in game.py)
        for solid in staticSolids:
            self.collisionsCalculated = self.collisionsCalculated + 1
            if solid.willCollide(self.rect, deltaH, deltaV):
                if deltaH > 0: self.resolveXGap(solid, solid.rect.left - self.rect.right, deltaV, 1)
                if deltaH < 0: self.resolveXGap(solid, self.rect.left - solid.rect.right, deltaV, -1)
                if deltaV > 0: self.resolveYGap(solid, solid.rect.top - self.rect.bottom, deltaH, 1)
                if deltaV < 0: self.resolveYGap(solid, self.rect.top - solid.rect.bottom, deltaH, -1)
                willNotCollide = False
        if willNotCollide:
            self.rect.move_ip(deltaH, deltaV)
        
        # for permeable in withPermeables:
        #     self.collisionsCalculated = self.collisionsCalculated + 1
        #     permeable.didCollide(self.rect)
        

        self.checkQuadTreeCollisions(quadTree)
    
    #TODO: Set this check, and the quadtree drawing logic to ON only when DEBUG is true (at some point)
    #This is only used for checking collisions with any of the quadtreenodes for now
    #For the purposes of updating the visual border (for development purposes)
    def checkQuadTreeCollisions(self, root: quadtreenode.QuadTreeNode):
        if root is None: return

        root.quad.didCollide(self.rect)
        self.quadTreeCollisisionCalculated = self.quadTreeCollisisionCalculated + 1
        for child in root.children:
            self.checkQuadTreeCollisions(child)

    # Its possible that multiple sets of collidables can be returned from the various bottom levels.
    # If the player is touching all 4 bottom level quads, they will all want to return their solids.
    # We don't want to duplicate entries though - because if that was the case we add a 4 constant multiplier
    # to our upper bounded worse case scenario (since 4 quads all with the same list of collidables would return 4 x that amount)
    # TODO: For unmoving collidables, we only want to add these solids if they don't already exist in the results.
    def findStaticCollidablesInQuadTree(self, root: quadtreenode.QuadTreeNode, added: set, result):
        if root is None: return result

        #If we got here, if the node has collidables, it has to be the bottom level.
        #So we want to append to the result but only if the result doesn't exist
        # ** Important to remember and understand: Any group of bottom level nodes in a single frame, while
        # we traverse the tree to get the solids, there should only be a single result to check on.
        if len(root.collidables) > 0:
            for solid in root.collidables:
                result.append(solid)
                # key = id(solid)
                # #If solid's memory address does exists in the set, mark it added, add to the result
                # if not(key in added):
                #     print(f"added key: {key}")
                #     added.add(key)
                #     result.append(solid)

        for child in root.children:
            #ONLY recur down if this player, this rect, collides with the child.
            if child is not None:
                childQuad: collidable.Collidable = child.quad
                if(childQuad.didCollide(self.rect)): return self.findStaticCollidablesInQuadTree(child, added, result)
        return result


    
    def resolveXGap(self, withCollidable: collidable.Collidable, distance: float, deltaV: float, dir: int):
        # Resolve gap down to one pixel
        x = distance - 2
        if(x > 0): self.rect.move_ip(dir*x, deltaV)

    def resolveYGap(self, withCollidable: collidable.Collidable, distance: float, deltaH: float, dir: int):
        # Resolve gap down to one pixel
        y = distance - 2
        if(y > 0): self.rect.move_ip(deltaH, dir*y)

    def storePreviousPosition(self):
        self.prevX = self.rect.x
        self.prevY = self.rect.y

    def setDidMove(self):
        self.xChangedPositive = self.rect.x > self.prevX
        self.xChangedNegative = self.rect.x < self.prevX
        self.yChangedPositive = self.rect.y > self.prevY
        self.yChangedNegative = self.rect.y < self.prevY

    # This seems to work (at least when we're not using delta to scale movements, need to verify)
    def didMoveUp(self):
        return self.yChangedNegative
    def didMoveDown(self):
        return self.yChangedPositive
    def didMoveLeft(self):
        return self.xChangedNegative
    def didMoveRight(self):
        return self.xChangedPositive

    def processMovementWithKeyEventTypes(self, event, eventType):
        if event.type == eventType:
            pressedValue = eventType == pygame.KEYDOWN
            if event.key == pygame.K_w:
                self.playerKeysPressed[globals.PressedKeys.UP] = pressedValue
            if event.key == pygame.K_s:
                self.playerKeysPressed[globals.PressedKeys.DOWN] = pressedValue
            if event.key == pygame.K_a:
                self.playerKeysPressed[globals.PressedKeys.LEFT] = pressedValue
            if event.key == pygame.K_d:
                self.playerKeysPressed[globals.PressedKeys.RIGHT] = pressedValue

    def processQuitGameConditions(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    def hasValidLeftInput(self):
        return self.playerKeysPressed[globals.PressedKeys.LEFT] and not self.playerKeysPressed[globals.PressedKeys.RIGHT]
    def hasValidRightInput(self):
        return self.playerKeysPressed[globals.PressedKeys.RIGHT] and not self.playerKeysPressed[globals.PressedKeys.LEFT]
    def hasValidUpInput(self):
        return self.playerKeysPressed[globals.PressedKeys.UP] and not self.playerKeysPressed[globals.PressedKeys.DOWN]
    def hasValidDownInput(self):
        return self.playerKeysPressed[globals.PressedKeys.DOWN] and not self.playerKeysPressed[globals.PressedKeys.UP]