import math
from random import choice

import pygame

from constants import *
from classes import *

def load_tilemap(tilemap : list[list[int]]):
    '''загружает препятствия уровня из tilemap'''
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
    '''очищает экран для перехода на следующий уровень'''
    wood_tiles.empty()
    iron_tiles.empty()
    tiles.empty()
    balls.empty()
    targets.empty()
    all_sprites.empty()
    global bullet
    bullet = 0

def change_level_animation():
    '''
    анимация смены экрана - пока что только текст
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global finished
            finished = True
    clock.tick(FPS)
    screen.fill(WHITE)
    Text = CLF.render('Вы прошли уровень ' + str(level), 0, BLACK)
    if bullet == 1:
        Text2 = CLF.render('за ' + str(bullet) + ' Выстрел', 0, BLACK)
    elif bullet <=4:
        Text2 = CLF.render('за ' + str(bullet) + ' Выстрелa', 0, BLACK)
    else:
        Text2 = CLF.render('за ' + str(bullet) + ' Выстрелов', 0, BLACK)
    Text_rect = Text.get_rect(center = screen.get_rect().center)
    Text2_rect = Text2.get_rect(center = (screen.get_rect().centerx, screen.get_rect().centery + Text.get_height()))
    screen.blit(Text, Text_rect)
    screen.blit(Text2, Text2_rect)
    gun.draw(screen)
    pygame.display.update()

def initiate_screen(level):
    '''
    готовит цели и клетки на следующий уровень
    '''
    try:
        level_num = LEVEL_TARGET_COUNT[level]
        level_rad = LEVEL_RADIUS[level]
        level_pos = LEVEL_SPAWNS[level]
        load_tilemap(LEVEL_TILEMAP[level])

    except:
        '''фикс для уровня больше запроганных, '''
        level_num = 5
        level_rad = [10, 10, 10, 10, 10]
        level_pos = [(600, 200), (600, 100), (600, 300), (600, 400), (600, 500)]
        load_tilemap(LEVEL_TILEMAP[0])
    for i in range(level_num):
        target = CrawlTarget(level_rad[i], level_pos[i])
        target.add(targets, all_sprites)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0

wood_tiles = pygame.sprite.Group()
iron_tiles = pygame.sprite.Group()
tiles = pygame.sprite.Group()
balls = pygame.sprite.Group()
targets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

background = Background()
gun = Gun()
clock = pygame.time.Clock()


finished = False
level = 1
initiate_screen(level)

while not finished:
    clock.tick(FPS)
    '''обработка ивентов'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            new_ball = gun.fire2_end(event)
            new_ball.add(balls, all_sprites)
            bullet +=1
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    '''смена положений спрайтов и пушки, увеличение силы пушки'''
    gun.update()
    all_sprites.update(screen, tiles)

    '''тест на поражение целей'''
    for b in balls:
        for t in targets:
            if b.hittest(t):
                t.remove(targets, all_sprites)

    '''прорисовка'''
    screen.fill(WHITE)
    gun.draw(screen)
    background.draw(screen)
    all_sprites.draw(screen)
    pygame.display.update()

    '''переход на следующий уровень при смерти всех целей'''
    if len(targets) == 0:
        for i in range(int(FPS*1.5)):
            if finished:
                break
            change_level_animation()
        screen_wipe()
        level += 1
        initiate_screen(level)


pygame.quit()
