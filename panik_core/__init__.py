import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

print("Hello From Panik Studios\nWelcome to Panik-Core Engine V0.8.0")

import pygame
from pygame.locals import *
import pygame_gui

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.font.init()
pygame.init()


from panik_core.window import *
from panik_core.game_object import *
from panik_core.assets import *
from panik_core.ui import *

# ^^^^^^^^^^^ Import submodules


QUIT = pygame.QUIT
BUTTON_CLICKED = pygame_gui.UI_BUTTON_PRESSED
BUTTON_DOUBLE_CLICKED = pygame_gui.UI_BUTTON_DOUBLE_CLICKED
BUTTON_START_PRESS = pygame_gui.UI_BUTTON_START_PRESS
BUTTON_HOVERED = pygame_gui.UI_BUTTON_ON_HOVERED
BUTTON_UNHOVERED = pygame_gui.UI_BUTTON_ON_UNHOVERED
TEXT_BOX_LINK_CLICKED = pygame_gui.UI_TEXT_BOX_LINK_CLICKED
TEXT_ENTRY_CHANGED = pygame_gui.UI_TEXT_ENTRY_CHANGED
TEXT_ENTRY_FINISHED = pygame_gui.UI_TEXT_ENTRY_FINISHED
DROP_DOWN_MENU_CHANGED = pygame_gui.UI_DROP_DOWN_MENU_CHANGED
HORIZONTAL_SLIDER_MOVED = pygame_gui.UI_HORIZONTAL_SLIDER_MOVED
SELECTION_LIST_NEW_SELECTION = pygame_gui.UI_SELECTION_LIST_NEW_SELECTION
SELECTION_LIST_REMOVE_SELECTION = pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION
SELECTION_LIST_DOUBLE_SELECT = pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION
DIALOG_CONFIRMED = pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED
PATH_SELECTED = pygame_gui.UI_FILE_DIALOG_PATH_PICKED
WINDOW_CLOSED = pygame_gui.UI_WINDOW_CLOSE
KEY_PRESSED = pygame.KEYDOWN
SCREENRESIZE = pygame.VIDEORESIZE

kA = pygame.K_a
kB = pygame.K_b
kC = pygame.K_c
kD = pygame.K_d
kE = pygame.K_e
kF = pygame.K_f
kG = pygame.K_g
kH = pygame.K_h
kI = pygame.K_i
kJ = pygame.K_j
kK = pygame.K_k
kL = pygame.K_l
kM = pygame.K_m
kN = pygame.K_n
kO = pygame.K_o
kP = pygame.K_p
kQ = pygame.K_q
kR = pygame.K_r
kS = pygame.K_s
kT = pygame.K_t
kU = pygame.K_u
kV = pygame.K_v
kW = pygame.K_w
kX = pygame.K_x
kY = pygame.K_y
kZ = pygame.K_z
kUP = pygame.K_UP
kLEFT = pygame.K_LEFT
kDOWN = pygame.K_DOWN
kRIGHT = pygame.K_RIGHT
kTAB = pygame.K_TAB
kSHIFT = pygame.K_LSHIFT
kESC = pygame.K_ESCAPE
kSPACE = pygame.K_SPACE
kCTRL = pygame.K_LCTRL
k0 = pygame.K_0
k1 = pygame.K_1
k2 = pygame.K_2
k3 = pygame.K_3
k4 = pygame.K_4
k5 = pygame.K_5
k6 = pygame.K_6
k7 = pygame.K_7
k8 = pygame.K_8
k9 = pygame.K_9
kF1 = pygame.K_F1
kF2 = pygame.K_F2
kF3 = pygame.K_F3
kF4 = pygame.K_F4
kF5 = pygame.K_F5
kF6 = pygame.K_F6
kF7 = pygame.K_F7
kF8 = pygame.K_F8
kF9 = pygame.K_F9
kF10 = pygame.K_F10
kF11 = pygame.K_F11
kF12 = pygame.K_F12


class Events:
    def get():
        return pygame.event.get()


class Keys:
    def get():
        return pygame.key.get_pressed()


def quit():
    pygame.quit()
    sys.exit()
