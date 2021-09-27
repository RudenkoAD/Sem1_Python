import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

#background
rect(screen, (255, 255, 255), (0, 0, 400, 400))

#face
circle(screen, (255, 255, 0), (200, 200), 100)

#eyes
circle(screen, (255, 0, 0), (160, 175), 25)
circle(screen, (255, 0, 0), (240, 175), 15)

#pupils
circle(screen, (0, 0, 0), (160, 175), 10)
circle(screen, (0, 0, 0), (240, 175), 8)

#mouth
rect(screen, (0, 0, 0), (160, 240, 80, 20), 0)

#brows
polygon(screen, (0, 0, 0), [(240, 160), (300, 140), (298, 134), (238, 154)])
polygon(screen, (0, 0, 0), [(160, 150), (110, 140), (120, 130), (170, 140)])


#debug
for i in range(80):
	line(screen, (0, 0, 0), (i*5, 0), (i*5, 400), 1)
	line(screen, (0, 0, 0), (0, i*5), (400, i*5), 1)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
