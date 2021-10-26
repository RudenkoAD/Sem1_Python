import math
import random
from random import choice, randint
import pygame
from constants import *

class Background():
    def __init__(self):
        pass
    def draw(self, screen):
        pygame.draw.rect(screen, GREY, (100, 100, WIDTH-200, HEIGHT-200), 1)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x = 20, y = 450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        r = 10
        self.r = 10
        super().__init__()
        self.color = choice(GAME_COLORS)
        self.image = pygame.surface.Surface((2*r,2*r))
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, self.color, (r, r), r)
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = 0
        self.vy = 0
        self.live = 30

    def update(self, screen):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.rect = self.rect.move(self.vx, int(self.vy))
        self.vy += 0.5
        self.vx -= 0.2 * self.vx / abs(self.vx)
        if self.rect.right >= screen.get_width():
            self.rect.right = screen.get_width()
            self.vx = -self.vx

        if self.rect.bottom >= screen.get_height():
            self.rect.bottom = screen.get_height()
            self.vy = -self.vy/2

        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = -self.vy/2

        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx = -self.vx

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с объектом obj.

        Args:
            obj: Обьект, с которым проверяется столкновение, обязан иметь аттрибут rect
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (math.hypot(self.rect.center[0] - obj.rect.center[0], self.rect.center[1] - obj.rect.center[1]) <= self.r + obj.r):
            return True
        return False

class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450

    def fire2_start(self, event):
        '''
        начало зарядки мяча на выстрел
        '''
        self.f2_on = 1

    def fire2_end(self, event):
        """
        Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        self.update()
        new_ball = Ball(round(self.x + self.f2_power * math.cos(self.an)), round(self.y + self.f2_power * math.sin(self.an)))
        new_ball.vx = self.f2_power * math.cos(self.an)/2
        new_ball.vy = self.f2_power * math.sin(self.an)/2
        self.f2_on = 0
        self.f2_power = 10
        return new_ball

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        self.an = math.atan2((-event.pos[1]+self.y), (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def update(self):
        self.power_up()
        self.image = pygame.surface.Surface((self.f2_power, 10))
        self.image.fill(self.color)
        pygame.draw.rect(self.image, BLACK, (0, 0, self.f2_power, 10), 1)
        self.rot_image = pygame.transform.rotate(self.image, math.degrees(self.an))
        self.rot_image.set_colorkey(BLACK)
        if self.an > 0:
            self.rot_rect = self.rot_image.get_rect(bottomleft=(self.x, self.y))
        else:
            self.rot_rect = self.rot_image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.rot_image, self.rot_rect)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

class Target(pygame.sprite.Sprite):
    def __init__(self):
        '''
        points - кол.во раз которое игрок попал в цель
        '''
        super().__init__()
        self.x = randint(100, 700)
        self.y = randint(100, 500)
        self.r = randint(2, 50)
        self.color = RED
        self.new_target()

    def draw(self, screen):
        '''вывод себя на экран'''
        screen.blit(self.image, self.rect)

    def new_target(self):
        """ Инициализация новой цели. """
        self.image = pygame.surface.Surface((2*self.r, 2*self.r))
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, self.color, (self.r, self.r), self.r)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.mask = pygame.mask.from_surface(self.image)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

class CrawlTarget(Target):
    def __init__(self, r):
        super().__init__()
        self.vx = 0
        self.vy = 0
        self.r = r
        self.new_target()
    def update(self, screen):
        self.rect = self.rect.move(self.vx, self.vy)
        self.vx += randint(-1 ,1)
        self.vy += randint(-1, 1)
        if self.rect.right >= screen.get_width()-100:
            self.rect.right = screen.get_width()-100
            self.vx = -self.vx/2

        if self.rect.bottom >= screen.get_height()-100:
            self.rect.bottom = screen.get_height()-100
            self.vy = -self.vy/2

        if self.rect.top <= 100:
            self.rect.top = 100
            self.vy = -self.vy/2

        if self.rect.left <= 100:
            self.rect.left = 100
            self.vx = -self.vx/2