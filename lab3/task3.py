import pygame
from pygame import color
from pygame.draw import *
from pygame import transform
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))


def background(surface):
    '''
    Фунция рисования фона
    surface - объект pygame.Surface
    '''
    rect(surface, (100, 200, 255), (0, 0, 400, 400))
    rect(surface, (0, 0, 255), (0, 200, 400, 400))
    rect(surface, (255, 255, 0), (0, 300, 400, 400))


def clouds(surface, color, x, y, radius):
    '''
    Функция рисует облака
    surface - объект pygame.Surface
    color - цвет, заданный в формате, подходящем для pygame.Color
    x, y - координаты левого верхнего угла
    r - радиус кружков, из которых состоят облака
    '''
    scale = radius / 16
    surface_clouds = pygame.Surface((100, 100), pygame.Color(1, 1, 1))
    for i, j in [(22, 16), (34, 16), (46, 16), (16, 28), (28, 28), (38, 28), (52, 28)]:
        circle(surface_clouds, color, (i, j), 16)
    surface_clouds.set_colorkey((1, 1, 1))
    surface_clouds = transform.rotozoom(surface_clouds, 0, scale)
    surface.blit(surface_clouds, (x, y))


def sunscreen(screen, color_leg, color_umbrella, x, y, h):
    sunscreen_surface = pygame.Surface((150, 100), pygame.Color(1, 1, 1))
    """
    Функция рисует зонтик
    screen -  объект pygame.Surface
    color - цвет, заданный в формате, подходящем для pygame.Color
    x, y - координаты левого верхнего угла
    """
    rect(sunscreen_surface, color_leg, (45, 30, 10, 100), 0)
    polygon(sunscreen_surface, color_umbrella, [(0, 30), (50, 0), (100, 30)])
    for i in range(0, 101, 20):
        line(sunscreen_surface, (0, 0, 0), (50, 0), (i, 30), 2)
    sunscreen_surface.set_colorkey((1, 1, 1))
    sunscreen_surface = transform.rotozoom(sunscreen_surface, 0, 1)
    screen.blit(sunscreen_surface, (x, y))


def boat(surface, x, y, l, color_boat, color_mast, color_windsail):
    """
    Функция рисует парусник
    surface -  объект pygame.Surface
    x, y - координаты левого верхнего угла
    l - длина лодки по оси X
    color_boat - цвет корпуса, заданный в формате, подходящем для pygame.Color
    color_mast - цвет мачты, заданный в формате, подходящем для pygame.Color
    color_windsail - цвет паруса, заданный в формате, подходящем для pygame.Color
    """
    surface_boat = pygame.Surface((140, 90), pygame.Color(1, 1, 1))
    scale = l / 140
    # корпус
    for color, width in [((0, 0, 0), 1), (color_boat, 0)]:
        polygon(surface_boat, color, [
                (20, 90), (100, 90), (140, 70), (0, 70)], width)

    # мачта
    rect(surface_boat, color_mast, (45, 0, 5, 70))

    # парус
    for color, width in [((0, 0, 0), 1), (color_windsail, 0)]:
        polygon(surface_boat, color, [
                (50, 0), (90, 30), (50, 60), (60, 30)], width)
    line(surface_boat, (0, 0, 0), (90, 30), (60, 30), 1)
    surface_boat.set_colorkey((1, 1, 1))
    surface_boat = transform.rotozoom(surface_boat, 0, scale)
    surface.blit(surface_boat, (x, y))


def main(screen):
    """
    Функция которая выводит всю картинку целиком
    screen - объект pygame.Surface
    """
    background(screen)
    clouds(screen, (255, 255, 255), 50, 50, 16)
    # sun
    circle(screen, (255, 255, 0), (360, 50), 35)
    sunscreen(screen, (100, 40, 30), (200, 77, 58), 80, 260, 130)
    boat(screen, 260, 80, 140, (200, 77, 58), (0, 0, 0), (157, 193, 131))


main(screen)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
