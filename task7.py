import turtle as T
import numpy as np
T.shape()
T.shapesize(1)


r = 30
k = 20

while True:
    dL=np.sqrt(r**2+k**2)/100
    da=(k+1)/r/100
    T.forward(dL)
    T.left(da*360/2/np.pi)
    r+=k/100