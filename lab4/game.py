import pygame
from pygame.draw import *
from random import randint
pygame.init()

global starttime, ballspeed, ballrad
starttime = 30
ballspeed = 10
ballrad = (15, 30)

global screen_height, screen_width
screen_height = 800
screen_width = 1200
FPS = 60

screen = pygame.display.set_mode((screen_width, screen_height))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

global COLORS
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

font = pygame.font.SysFont('nimbussans', 100)

class Ball: 
	
	def __init__(self):
		self.x = randint(100, 1100)
		self.y = randint(100, 900)
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
		
class Counter:
	
	def __init__(self, count, cords = (0, 0)):
		self.count=count
		self.cords=cords
		self.font = pygame.font.SysFont('nimbussans', 30)
		
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

#startup
name = input('please enter your name:')


#setting up balls and other stuff
balls = []
for i in range(10):
	ball=Ball()
	balls.append(ball)

background = Background()

pygame.display.update()
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
finished = False

while not finished:
	
	clock.tick(FPS)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			x = event.pos[0]
			y = event.pos[1]
			for ball in balls:
				if (ball.x - x)**2 + (ball.y - y)**2 < ball.rad**2:
					balls.remove(ball)
					background.score.count+=1
					newball=Ball()
					balls.append(newball)
		elif event.type == pygame.USEREVENT:
			background.time.count-=1
			if background.time.count == 0:
				finished=True
	
	screen.fill(BLACK)
	for ball in balls:
		ball.update()
	background.update()
	
	pygame.display.update()

#записать:
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

while True:		
	screen.fill(BLACK)
	num = font.render(str(background.score.count), 0, COLORS[2])
	text = font.render('Финальный Счёт:', 0, COLORS[3])
	
	screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - 101))
	screen.blit(num, (screen_width/2 - num.get_width()/2, screen_height/2))
	
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	
	
	





