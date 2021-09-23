import turtle as T
import numpy as np
T.shape('turtle')
T.speed(10)


J=2
while True:
    T.circle(5*J)
    T.right(180)
    T.circle(5*J)
    T.right(180)
    J+=1
