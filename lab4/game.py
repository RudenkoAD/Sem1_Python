import math

import pygame
from pygame.draw import *
from random import randint
import configparser
from math import sin, cos

pygame.init()

config = configparser.ConfigParser()
config.read('options.ini')

global screen_height, screen_width
screen_height = int(config['Screen']['screen_height'])
screen_width = int(config['Screen']['screen_width'])
FPS = int(config['Screen']['FPS'])

global COLORS, GameFont
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE, BLACK, GREY]
GameFont = pygame.font.SysFont('nimbussans', 100)


class Name_Input:
    def __init__(self, default, cords, size, color_inactive=COLORS[7], color_active=COLORS[8]):
        self.cords = cords
        self.size = size
        self.rect = pygame.Rect(cords, size)
        self.font = pygame.font.SysFont('nimbussans', 50)
        self.active = False
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.text = ''
        self.default = default

    def update(self):
        if not self.active and self.text == '':
            self.textsurf = self.font.render(self.default, 1, COLORS[6])
            self.textsurf.set_alpha(100)
        else:
            self.textsurf = self.font.render(self.text, 1, COLORS[6])
        self.textsize = self.textsurf.get_size()
        x0 = self.size[0] - self.textsize[0]
        y0 = self.size[1] - self.textsize[1]
        self.surface = pygame.Surface(self.size)
        if self.active:
            bg = self.color_active
        else:
            bg = self.color_inactive
        self.surface.fill(bg)
        self.surface.blit(self.textsurf, (x0 / 2, y0 / 2))
        screen.blit(self.surface, self.cords)

    def edit(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.active = False
            else:
                self.text += event.unicode

    def checkclick(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False



class Square:

    def __init__(self, rot_speed):
        self.center_x = randint(screen_width * 2 / 10, screen_width * 8 / 10)
        self.center_y = randint(screen_height * 2 / 10, screen_height * 8 / 10)
        self.rotation = randint(0, 360)
        self.rot_speed = rot_speed
        self.size = 2 * randint(ballrad[0], ballrad[1])
        self.radius = 20 * randint(ballspeed, ballspeed)
        self.color = COLORS[randint(0, 5)]
        self.image = pygame.surface.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self):
        self.rotation += self.rot_speed
        self.x = self.center_x + self.radius * cos(self.rotation/360 * 2 * math.pi)
        self.y = self.center_y + self.radius * sin(self.rotation/360 * 2 * math.pi)
        self.rect.center = self.x, self.y

    def draw(self ,surface):
        surface.blit(self.image, self.rect)

    def checkclick(self, pos):
        if abs(self.x - pos[0]) < self.size/2 and abs(self.y - pos[1]) < self.size/2:
            return True
        return False


class Ball:

    def __init__(self):
        self.x = randint(screen_width / 10, screen_width * 9 / 10)
        self.y = randint(screen_height / 10, screen_height * 9 / 10)
        self.rad = randint(ballrad[0], ballrad[1])
        self.speed = [randint(-ballspeed, ballspeed), randint(ballspeed, ballspeed)]
        self.color = COLORS[randint(0, 5)]

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]
        circle(screen, self.color, (self.x, self.y), self.rad)
        if self.x <= 0 or self.x >= screen_width:
            self.speed[0] = -self.speed[0]
        if self.y <= 0 or self.y >= screen_height:
            self.speed[1] = -self.speed[1]

    def checkclick(self, pos):
        x, y = pos
        if (self.x - x) ** 2 + (self.y - y) ** 2 < self.rad ** 2:
            return True
        return False


class Counter:

    def __init__(self, count, cords=(0, 0)):
        self.count = count
        self.cords = cords
        self.font = pygame.font.SysFont('nimbussans', 30)

    def update(self):
        num = self.font.render(str(self.count), 0, COLORS[1])

        width, height = int(num.get_width() + 20), int(num.get_height() + 12)
        num_in_rect = pygame.Surface((width, height))

        rect(num_in_rect, COLORS[2], (5, 5, num.get_width() + 10, num.get_height() + 2), 5)
        num_in_rect.blit(num, (10, 10))
        screen.blit(num_in_rect, self.cords)


class Background:

    def __init__(self):
        self.font = pygame.font.SysFont('nimbussans', 30)
        self.score = Counter(0, (115, 0))
        self.time = Counter(starttime, (115, 43))

    def update(self):
        score_text = self.font.render(' СЧЁТ:', 0, COLORS[1])  # width = 115
        time_text = self.font.render('ВРЕМЯ:', 0, COLORS[1])  # width = 115

        self.time.update()
        self.score.update()

        screen.blit(score_text, (20, 10))
        screen.blit(time_text, (0, 51))


class Button:
    '''
    x, y - coords of left upper corner
    color - a pygame.color object for the text on the button
    bg - a pygame.color object for the background of the button
    text - the text on the button
    size - the dimensions of the button
    rect - the bounding box of the button
    '''

    def __init__(self, text, Id, pos, size, color=COLORS[6], bg=COLORS[7]):
        self.id = Id
        self.font = GameFont
        self.x, self.y = pos
        self.size = size
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.set_text(color, bg)

    def set_text(self, color, bg):
        self.textsurf = self.font.render(self.text, 1, color)
        self.textsize = self.textsurf.get_size()
        x0 = self.size[0] - self.textsize[0]
        y0 = self.size[1] - self.textsize[1]
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.textsurf, (x0 / 2, y0 / 2))

    def update(self):
        screen.blit(self.surface, (self.x, self.y))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover()

    def hover(self):
        rect(screen, COLORS[1], (self.x, self.y, self.size[0], self.size[1]), width=2)

    def checkclick(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False


# leaderboard settings:
def leaderboard(name, score):
    if name == '':
        return 0
    with open('leaderboard.txt', 'r') as f:
        massiv = f.read().split('\n')
        for i in range(len(massiv)):
            massiv[i] = massiv[i].split(' ')
        massiv.append([name, str(score)])
        massiv.sort(key=lambda x: -int(x[1]))
        print(massiv)
        massiv.pop()
        space = ' '
        newline = '\n'
        for i in range(len(massiv)):
            massiv[i] = space.join(massiv[i])
    with open('leaderboard.txt', 'w') as f:
        f.write(newline.join(massiv))


# startup
finished = False
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# initiating menu screen
easy = Button('Easy', 0, (450, 100), (300, 100))
medium = Button('Medium', 1, (450, 300), (300, 100))
hard = Button('Hard', 2, (450, 500), (300, 100))
menu_buttons = [easy, medium, hard]
input_name = Name_Input('Your name here...', (450, 650), (300, 50))

# initianting game screen and setting the game difficulty
global starttime, ballspeed, ballrad, score_multi
starttime, ballspeed, ballrad, score_multi = (0, 0, 0, 0)

# initiating final screen
new_game = Button('Play Again?', 3, (400, 501), (400, 100))
final_buttons = [new_game]


def Initiate_Game():
    balls = []
    for i in range(10):
        ball = Ball()
        balls.append(ball)
    squares = []
    background = Background()
    pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    pygame.time.set_timer(pygame.USEREVENT + 1, 3000)
    return balls, squares, background


def Initiate_Final():
    num = GameFont.render(str(background.score.count), 0, COLORS[2])
    text = GameFont.render('Финальный Счёт:', 0, COLORS[3])
    return num, text


# settings for the loop
In_Menu = True
In_Game = False
In_Final_Screen = False

# Loop
while not finished:

    if In_Menu:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    for button in menu_buttons:
                        if button.checkclick(pos):
                            starttime = int(config[button.text]['starttime'])
                            ballspeed = int(config[button.text]['ballspeed'])
                            ballrad = (int(config[button.text]['ballradmin']), int(config[button.text]['ballradmax']))
                            ball_score = int(config[button.text]['ball_score'])
                            square_score = int(config[button.text]['square_score'])
                            square_rot_speed = int(config[button.text]['square_rot_speed'])
                            balls, squares, background = Initiate_Game()
                            name = input_name.text
                            In_Menu = False
                            In_Game = True
                    if input_name.checkclick(pos):
                        input_name.active = True
            elif event.type == pygame.KEYDOWN:
                input_name.edit(event)
        screen.fill(BLACK)
        for button in menu_buttons:
            button.update()
        input_name.update()
        pygame.display.update()

    if In_Game:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                cords = pygame.mouse.get_pos()
                for ball in balls:
                    if ball.checkclick(cords):
                        balls.remove(ball)
                        background.score.count += ball_score
                        newball = Ball()
                        balls.append(newball)

                for square in squares:
                    if square.checkclick(cords):
                        squares.remove(square)
                        background.score.count += square_score

            elif event.type == pygame.USEREVENT + 1:
                squares = []
                newsquare = Square(square_rot_speed)
                squares.append(newsquare)

            elif event.type == pygame.USEREVENT:
                background.time.count -= 1
                if background.time.count == 0:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                    In_Game = False
                    In_Final_Screen = True
                    num, text = Initiate_Final()
                    leaderboard(name, background.score.count)
        screen.fill(BLACK)
        for ball in balls:
            ball.update()
        for square in squares:
            square.update()
            square.draw(screen)
        background.update()
        pygame.display.update()

    if In_Final_Screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    for button in final_buttons:
                        if button.checkclick(pos):
                            if button.id == 3:
                                In_Final_Screen = False
                                In_Menu = True
        screen.fill(BLACK)
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - 101))
        screen.blit(num, (screen_width / 2 - num.get_width() / 2, screen_height / 2))
        for button in final_buttons:
            button.update()
        pygame.display.update()

pygame.quit
