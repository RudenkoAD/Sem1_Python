import random as rd
import turtle as t
t.speed(1)

def run(pos1, pos2, step, y):
	for z in y:
		x = z.split()
		if x==['d']:
			t.pendown()
		elif x==['u']:
			t.penup()
		else:
			pos1 = pos1 + step * int(x[0])
			pos2 = pos2 + step * int(x[1])
			t.goto(pos1, pos2)
	return pos1, pos2

f = open('instructions.txt', 'r')
Manual = f.read().split('~')
print(Manual)
for i in range(len(Manual)):
	Manual[i]=Manual[i].strip().split('\n')
print(Manual)
instruction=list(map(int, input().split()))
c1, c2=0, 0
for ins in instruction:
	c1, c2 = run(c1, c2, 10, Manual[ins])
	t.goto(c1+10, c2)
	c1, c2 = c1+10, c2
	t.pendown()
