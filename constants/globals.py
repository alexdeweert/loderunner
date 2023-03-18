import pygame
from enum import IntEnum

def init():
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
    
    SCREEN_W = 800
    SCREEN_H = 600
    H_SPEED = 1
    V_SPEED = 1
    FPS = 30
    MAX_DELTA = 1/FPS
    FPS_DISP_X = SCREEN_W-25
    FPS_DISP_Y = 0
    DEBUG_FONT = pygame.font.SysFont("Arial", 18)
    DEBUG_FONT_COLOR = pygame.Color("Coral")
    PLAYER_W = 32
    PLAYER_H = 32
    SCREEN_CAPTION = "Loderunner"
    ZERO = 0
    ONE = 1
    SECOND_MS = 1000

class PressedKeys(IntEnum):
        LEFT = 0,
        RIGHT = 1,
        UP = 2,
        DOWN = 3

globals().update(PressedKeys.__members__)