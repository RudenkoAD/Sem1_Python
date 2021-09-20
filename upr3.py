import turtle as t
t.speed(0)
t.screensize(10000, 10000)
Vx=5.00
Vy=40.00
ay=-1.00
x, y = 0.00, 0.00
t.forward(4000)
t.backward(4000)
dt=0.5
for L in range(1, 1000000):
	x += Vx*dt
	y += Vy*dt
	Vy += ay*dt
	if y<=0:
		y = 0.00
		Vy = -Vy*0.90
	t.goto(x, y)

