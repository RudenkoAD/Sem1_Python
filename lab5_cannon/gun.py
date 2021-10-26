import math
from random import choice

import pygame

from constants import *
from classes import *

def screen_wipe():
    balls.empty()
    all_sprites.empty()
    targets.empty()
    global bullet
    bullet = 0

def change_level_animation():
    '''

    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    clock.tick(FPS)
    screen.fill(WHITE)
    Text = CLF.render('Вы прошли уровень ' + str(level) + '\nза ' + str(bullet) + ' Выстрелов', 0, BLACK)
    Text_rect = Text.get_rect(center = screen.get_rect().center)
    screen.blit(Text, Text_rect)
    gun.draw(screen)
    pygame.display.update()

def initiate_screen(level):
    '''
    готовит цели на следующий уровень
    #FIXME и стенки
    '''
    try:
        level_num = LEVEL_TARGET_COUNT[level]
        level_rad = LEVEL_RADIUS[level]
    except:
        level_num = 5
        level_rad = [10, 10, 10, 10, 10]
    for i in range(level_num):
        target = CrawlTarget(level_rad[i])
        target.add(targets, all_sprites)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0

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
    all_sprites.update(screen)

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
        for i in range(FPS*3):
            if finished:
                break
            change_level_animation()
        screen_wipe()
        level += 1
        initiate_screen(level)


pygame.quit()
