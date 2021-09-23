import turtle as T
import math as m

T.ht()
T.speed(10)
T.radians()
def star(n, r): #n - кол-во вершин, r - радиус опис. окружности
    step = r * 2 * m.cos(m.pi / n/2)

    T.penup()
    T.bk(r)
    T.left(m.pi/n/2)
    T.pendown()
    
    for i in range(n):
        T.fd(step)
        T.right(m.pi - m.pi/n)

    T.penup()
    T.right(m.pi/n/2)
    T.fd(r)
    T.pendown()

star(5, 40)
T.penup()
T.fd(100)
T.pendown()
star(11, 40)
