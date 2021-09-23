import turtle as T
T.shape('turtle')

for J in range(1, 11):
    for i in range(4):
        T.forward(50+10*J)
        T.right(90)
    T.penup()
    T.goto(-5*J, 5*J)
    T.pendown()

while True:
    T.left(1)