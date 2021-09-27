import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

#background
rect(screen, (100, 200, 255), (0, 0, 400, 400))
rect(screen, (0, 0, 255), (0, 200, 400, 400))
rect(screen, (255, 255, 0), (0, 300, 400, 400))

#clouds
circle(screen, (255, 255, 255), (50, 50), 16)
circle(screen, (255, 255, 255), (62, 50), 16)
circle(screen, (255, 255, 255), (74, 50), 16)
circle(screen, (255, 255, 255), (44, 62), 16)
circle(screen, (255, 255, 255), (56, 62), 16)
circle(screen, (255, 255, 255), (68, 62), 16)
circle(screen, (255, 255, 255), (80, 62), 16)

#sun
circle(screen, (255, 255, 0), (360, 50), 35)

#sunscreen
rect(screen, (100, 40, 30), (125, 290, 10, 100), 0)
polygon(screen, (200, 77, 58), [(80, 290), (130, 260), (180, 290)])
line(screen, (0, 0, 0), (130, 260), (180, 290), 2)
line(screen, (0, 0, 0), (130, 260), (160, 290), 2)
line(screen, (0, 0, 0), (130, 260), (140, 290), 2)
line(screen, (0, 0, 0), (130, 260), (120, 290), 2)
line(screen, (0, 0, 0), (130, 260), (100, 290), 2)
line(screen, (0, 0, 0), (130, 260), (80, 290), 2)

#boat
polygon(screen, (200, 77, 58), [(250, 270), (330, 270), (370, 250), (230, 250)])

polygon(screen, (0, 0, 0), [(250, 270), (330, 270), (370, 250), (230, 250)], 1)

#mast
polygon(screen, (0, 0, 0), [(275, 250), (280, 250), (280, 180), (275, 180)])

#windsail
polygon(screen, (157, 193, 131), [(280, 180), (320, 210), (280, 240), (290, 210)])
polygon(screen, (0, 0, 0), [(280, 180), (320, 210), (280, 240), (290, 210)], 1)
line(screen, (0, 0, 0), (320, 210), (290, 210), 1)

#debug
#for i in range(40):
#	line(screen, (0, 0, 0), (i*10, 0), (i*10, 400), 1)
#	line(screen, (0, 0, 0), (0, i*10), (400, i*10), 1)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
