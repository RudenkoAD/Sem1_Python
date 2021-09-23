import turtle as T
import numpy as np
T.shape('turtle')
T.speed(0)

#лицо
T.penup()
T.goto(0, -200)
T.pendown()
T.color("yellow")
T.begin_fill()
T.circle(200)
T.end_fill()

#правый глаз
T.penup()
T.goto(90, 80)
T.pendown()
T.color("blue")
T.begin_fill()
T.circle(20)
T.end_fill()

#левый глаз
T.penup()
T.goto(-90, 80)
T.pendown()
T.color("blue")
T.begin_fill()
T.circle(20)
T.end_fill()

#нос
T.penup()
T.goto(0, 0)
T.pendown()
T.color("black")
#T.seth(-90)
T.width(10)
T.goto(0, -60)
#T.fd(40)

#рот
T.penup()
T.goto(-80, -80)
T.right(90)
T.pendown()
T.color("red")
T.pensize(5)
T.circle(80, 180)




while True:
    T.left(1)
