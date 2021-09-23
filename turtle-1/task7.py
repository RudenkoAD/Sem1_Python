import turtle as T
import math as m
T.shape()
T.shapesize(1)
T.radians()

r = 30
k = 50

while True:
    dL=m.sqrt(r**2+k**2)/2/m.pi/10
    T.forward(dL)
    T.left(0.1)
    r+=k/2/m.pi/10
