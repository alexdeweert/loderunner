import pygame
from enum import IntEnum

def init():
    global DEBUG
    global SCREEN_W
    global SCREEN_H
    global H_SPEED
    global V_SPEED
    global FPS
    global MAX_DELTA
    global FPS_DISP_X
    global FPS_DISP_Y
    global DEBUG_FONT
    global DEBUG_FONT_COLOR
    global PLAYER_W
    global PLAYER_H
    global SCREEN_CAPTION
    global ZERO
    global ONE
    global SECOND_MS
    global SIMULATED_LAG_MS
    global QUAD_TREE_DEPTH
    global GRAVITY_SPEED
    
    DEBUG = True
    SCREEN_W = 1152
    SCREEN_H = 768
    H_SPEED = 250
    V_SPEED = 250
    SIMULATED_LAG_MS = 0
    FPS = 60
    MAX_DELTA = 1/FPS
    FPS_DISP_X = 10
    FPS_DISP_Y = 5
    DEBUG_FONT = pygame.font.SysFont("Arial", 12)
    DEBUG_FONT_COLOR = pygame.Color("Coral")
    PLAYER_W = 30
    PLAYER_H = 30
    SCREEN_CAPTION = "Loderunner"
    ZERO = 0
    ONE = 1
    SECOND_MS = 1000
    QUAD_TREE_DEPTH = 3
    GRAVITY_SPEED = 200

class PressedKeys(IntEnum):
        LEFT = 0,
        RIGHT = 1,
        UP = 2,
        DOWN = 3

class Quadrant(IntEnum):
        TOPLEFT = 0,
        TOPRIGHT = 1,
        BOTTOMLEFT = 2,
        BOTTOMRIGHT = 3

globals().update(PressedKeys.__members__)
globals().update(Quadrant.__members__)