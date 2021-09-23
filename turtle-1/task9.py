import turtle as T
import numpy as np
T.shape('turtle')
T.speed(0.2)

def nice(n, radius):
    T.penup()
    T.goto(radius, 0)
    T.pendown()
    T.setheading(0)
    T.left(180/n)
    step = 2*radius* np.sin(np.radians(180/n))
    for i in range(n):
        T.forward(step)
        T.left(360/n)

T.mode('logo')
T.degrees(360)
for J in range(3, 13):
    nice(J, 10*J)

