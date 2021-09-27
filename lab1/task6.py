import turtle as T
T.shape('turtle')

n=int(input())
b = 360/n

for i in range(n):
    T.forward(100)
    T.stamp()
    T.backward(100)
    T.right(b)

while True:
    T.left(1)