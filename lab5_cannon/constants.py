import pygame.font

FPS = 30

#colors for targets and bullets
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

#screen settings
WIDTH = 800
HEIGHT = 600

#font for animation between levels
pygame.font.init()
CLF=pygame.font.Font(pygame.font.match_font('comicsans'), 50)
LEVEL_TARGET_COUNT = [0, 1, 2, 3, 1, 3]
LEVEL_RADIUS = [0, [30], [20, 20], [30, 20, 20], [10], [10, 10, 10]]