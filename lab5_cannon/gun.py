import math
import sys
from random import choice

import pygame

from constants import *
from classes import *


def load_tilemap(tilemap: list[list[int]]):
    """загружает препятствия уровня из tilemap"""
    ycord = 20
    for y in range(len(tilemap)):
        xcord = 20
        for x in tilemap[y]:
            if x == 1:
                newtile = WoodTile((xcord, ycord))
                newtile.add(wood_tiles, tiles, all_sprites)
            elif x == 2:
                newtile = IronTile((xcord, ycord))
                newtile.add(iron_tiles, tiles, all_sprites)
            xcord += 40
        ycord += 40


def screen_wipe():
    """очищает экран для перехода на следующий уровень"""
    wood_tiles.empty()
    iron_tiles.empty()
    tiles.empty()
    balls.empty()
    targets.empty()
    all_sprites.empty()


def change_level_animation(bullet, level):
    """
    анимация смены экрана - пока что только текст
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(FPS)
    screen.fill(WHITE)
    text = CLF.render('Вы прошли уровень ' + str(level), 0, BLACK)
    if bullet == 1:
        text2 = CLF.render('за ' + str(bullet) + ' Выстрел', 0, BLACK)
    elif bullet <= 4:
        text2 = CLF.render('за ' + str(bullet) + ' Выстрелa', 0, BLACK)
    else:
        text2 = CLF.render('за ' + str(bullet) + ' Выстрелов', 0, BLACK)
    text_rect = text.get_rect(center=screen.get_rect().center)
    text2_rect = text2.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery + text.get_height()))
    screen.blit(text, text_rect)
    screen.blit(text2, text2_rect)
    pygame.display.update()


def initiate_screen(level):
    """
    готовит цели и клетки на следующий уровень
    """
    '''stationary targets'''
    for i in range(LEVEL_STATIC_COUNT[level]):
        target = StationaryTarget(LEVEL_STATIC_RADIUS[level][i], LEVEL_STATIC_COORDINATES[level][i])
        target.add(targets, all_sprites)
    '''path targets'''
    for i in range(LEVEL_PATH_COUNT[level]):
        target = PathTarget(
            LEVEL_PATH_RADIUS[level][i],
            LEVEL_PATH_COORDINATES[level][i][0],
            LEVEL_PATH_COORDINATES[level][i][1]
        )
        target.add(targets, all_sprites)
    '''tiles'''
    load_tilemap(LEVEL_TILEMAP[level])

"""создание экрана"""
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
"""создание меню"""
buttons = pygame.sprite.Group()
"""создание групп спрайтов и инициализация первых объектов"""
wood_tiles = pygame.sprite.Group()
iron_tiles = pygame.sprite.Group()
tiles = pygame.sprite.Group()
balls = pygame.sprite.Group()
targets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()
level = 1


def game_loop(level):
    gun = Gun()
    screen_wipe()
    initiate_screen(level)
    finished = False
    bullet = 0

    while not finished:
        clock.tick(FPS)

        '''обработка ивентов'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire2_start()
            elif event.type == pygame.MOUSEBUTTONUP:
                new_ball = gun.fire2_end(event)
                new_ball.add(balls, all_sprites)
                bullet += 1
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_loop()
                    if result == 'restart':
                        screen_wipe()
                        bullet = 0
                        initiate_screen(level)
                    elif result == 'exit':
                        finished = True

        '''смена положений спрайтов и пушки, увеличение силы пушки'''
        gun.update()
        all_sprites.update(screen, tiles)

        '''тест на поражение целей'''
        for b in balls:
            for t in targets:
                if b.hittest(t):
                    t.kill()

        '''прорисовка'''
        screen.fill(WHITE)
        gun.draw(screen)
        all_sprites.draw(screen)
        pygame.display.update()

        '''переход на следующий уровень при смерти всех целей'''
        if len(targets) == 0:
            for i in range(int(FPS * 1.5)):
                if finished:
                    break
                change_level_animation(bullet, level)
            screen_wipe()
            bullet = 0
            level += 1
            if level >= 5:
                finished = True
            initiate_screen(level)


def menu_loop():
    button_1 = Button('Играть', pygame.rect.Rect(300, 100, 200, 100))
    button_2 = Button('Выбор уровня', pygame.rect.Rect(200, 250, 400, 100))
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.get_click(event):
                    game_loop(1)
                if button_2.get_click(event):
                    level_choice_loop()

        screen.fill(WHITE)
        button_1.draw(screen)
        button_2.draw(screen)
        pygame.display.update()


def level_choice_loop():
    button_1 = Button('1', pygame.rect.Rect(200, 100, 50, 50))
    button_2 = Button('2', pygame.rect.Rect(250, 100, 50, 50))
    button_3 = Button('3', pygame.rect.Rect(300, 100, 50, 50))
    button_4 = Button('4', pygame.rect.Rect(350, 100, 50, 50))
    button_5 = Button('5', pygame.rect.Rect(400, 100, 50, 50))
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.get_click(event):
                    game_loop(1)
                elif button_2.get_click(event):
                    game_loop(2)
                elif button_3.get_click(event):
                    game_loop(3)
                elif button_4.get_click(event):
                    game_loop(4)
                elif button_5.get_click(event):
                    game_loop(5)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1

        screen.fill(WHITE)
        button_1.draw(screen)
        button_2.draw(screen)
        button_3.draw(screen)
        button_4.draw(screen)
        button_5.draw(screen)
        pygame.display.update()


def pause_loop():
    """Элементы меню паузы - они накладываются на экран с которого пауза была вызвана"""
    '''задний план игры с фильтром'''
    filtersurf = pygame.surface.Surface((WIDTH, HEIGHT))
    backbone = pygame.surface.Surface((WIDTH, HEIGHT))
    filtersurf.fill(BLACK)
    filtersurf.set_alpha(150)
    backbone.blit(screen, (0, 0))
    backbone.blit(filtersurf, (0, 0))
    '''кнопки'''
    button_exit = Button('Главное меню', pygame.rect.Rect(200, 150, 400, 100))
    button_restart = Button('Заново', pygame.rect.Rect(200, 250, 400, 100))
    button_continue = Button('Продолжить', pygame.rect.Rect(200, 350, 400, 100))

    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_exit.get_click(event):
                    return 'exit'
                if button_restart.get_click(event):
                    return 'restart'
                if button_continue.get_click(event):
                    return None
        screen.fill(WHITE)
        screen.blit(backbone, (0, 0))
        button_exit.draw(screen)
        button_restart.draw(screen)
        button_continue.draw(screen)
        pygame.display.update()


'''starting the game:'''
menu_loop()
pygame.quit()
