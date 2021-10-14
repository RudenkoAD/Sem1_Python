import pygame
from pygame.draw import *
from random import randint
pygame.init()

global screen_height, screen_width
screen_height = 800
screen_width = 1200
FPS = 60

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

global COLORS, GameFont
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE, BLACK]
GameFont = pygame.font.SysFont('nimbussans', 100)



class Ball: 
    
    def __init__(self):
        self.x = randint(100, 1100)
        self.y = randint(100, 700)
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
        if (self.x - x)**2 + (self.y - y)**2 < self.rad**2:
            return True
        return False
        
class Counter:
    
    def __init__(self, count, cords = (0, 0)):
        self.count=count
        self.cords=cords
        self.font = GameFont
        
    def update(self):
        num = self.font.render(str(self.count), 0, COLORS[1])
        
        width, height = int(num.get_width()+20), int(num.get_height()+12)
        num_in_rect=pygame.Surface((width, height))
        
        rect(num_in_rect, COLORS[2], (5, 5, num.get_width()+10, num.get_height()+2), 5)
        num_in_rect.blit(num, (10, 10))
        screen.blit(num_in_rect, self.cords)

class Background:
    
    def __init__(self):
        self.font = pygame.font.SysFont('nimbussans', 30)
        self.score = Counter(0, (115, 0))
        self.time = Counter(starttime, (115, 43))
    
    def update(self):
        score_text = self.font.render(' СЧЁТ:', 0, COLORS[1]) #width = 115
        time_text = self.font.render('ВРЕМЯ:', 0, COLORS[1]) #width = 115
        
        self.time.update()
        self.score.update() 
        
        screen.blit(score_text, (20, 10))
        screen.blit(time_text,  (0, 51))

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
        x0=self.size[0]-self.textsize[0]
        y0=self.size[1]-self.textsize[1]
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.textsurf, (x0/2, y0/2))
 
    def update(self):
        screen.blit(self.surface, (self.x, self.y))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover()

    def hover(self):
        rect(screen, COLORS[1], (self.x, self.y, self.size[0], self.size[1]), width = 2)
 
    def checkclick(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False






#startup
finished = False
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

#menu screen
In_Menu = True
#initiate menu buttons
easy = Button('Easy', 0, (450,100), (300, 100))
medium = Button('Medium', 1, (450,300), (300, 100))
hard = Button('Hard', 2, (450,500), (300, 100))
buttons = [easy, medium, hard]

#menu loop
while In_Menu and not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = event.pos
                for button in buttons:
                    if button.checkclick(pos):
                        dif_id = button.id
                        In_Menu = False
    screen.fill(BLACK)
    for button in buttons:
        button.update()
    pygame.display.update()

#initianting game screen and setting the game difficulty
if not finished:
    difset = [
    [30, 4, (20, 40), 1],
    [30, 8, (15, 30), 1.5],
    [30, 12, (10, 20), 2]
    ]
    global starttime, ballspeed, ballrad, score_multi
    starttime, ballspeed, ballrad, score_multi = difset[dif_id]
    In_Game = True
    
    balls = []
    for i in range(10):
        ball=Ball()
        balls.append(ball)
    background = Background()
    pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT, 1000)

#game loop
while In_Game and not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #cords = event.pos
            cords = pygame.mouse.get_pos()
            for ball in balls:
                if ball.checkclick(cords):
                    balls.remove(ball)
                    background.score.count+=score_multi
                    newball=Ball()
                    balls.append(newball)
 
        elif event.type == pygame.USEREVENT:
            background.time.count-=1
            if background.time.count == 0:
                In_Game=False
    
    screen.fill(BLACK)
    for ball in balls:
        ball.update()
    background.update()
    pygame.display.update()

#leaderboard update:
    #это жесть просто, я не знаю как это нормально делать, спасите
    '''
if not finished:                
        score = background.score.count
        with open('leaderboard.txt', 'r') as f:
                massiv = f.read().split('\n')
                for i in range(len(massiv)):
                        massiv[i]=massiv[i].split(' ')
                massiv.append([name, str(score)])
                massiv.sort(key =lambda x: -int(x[1]))
                print(massiv)
                massiv.pop()
                space=' '
                newline='\n'
                for i in range(len(massiv)):
                        massiv[i]=space.join(massiv[i])
        with open('leaderboard.txt', 'w') as f:
                f.write(newline.join(massiv))
                '''

#final screen:
while not finished:     
    screen.fill(BLACK)
    num = GameFont.render(str(background.score.count), 0, COLORS[2])
    text = GameFont.render('Финальный Счёт:', 0, COLORS[3])
    
    screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - 101))
    screen.blit(num, (screen_width/2 - num.get_width()/2, screen_height/2))
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished=True

pygame.quit
    
    





