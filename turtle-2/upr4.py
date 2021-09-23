from random import randint
import turtle


number_of_turtles = 10
steps_of_time_number = 10000
turtle.screensize(200, 200)
turtle.penup()
turtle.goto(-50, 50)
turtle.pendown()
turtle.goto(50,50)
turtle.goto(50, -50)
turtle.goto(-50, -50)
turtle.goto(-50, 50)
turtle.penup()
turtle.goto(-100, -100)
pool = [turtle.Turtle(shape='turtle') for i in range(number_of_turtles)]
for unit in pool:
	unit.penup()
	unit.speed(0)
	unit.shape('circle')
	unit.goto(randint(-50, 50), randint(-50, 50))
	unit.setheading(randint(0, 360))
	unit.resizemode("user")
	unit.shapesize(0.5, 0.5, 0)


for i in range(steps_of_time_number):
	for unit in pool:
		unit.forward(2)
		if unit.xcor()>50:
			unit.goto(50, unit.ycor())
			unit.setheading(180 - unit.heading())
		if unit.xcor() < -50:
			unit.goto(-50, unit.ycor())
			unit.setheading(180 - unit.heading())
		if unit.ycor() < -50:
			unit.goto(unit.xcor(), -50)
			unit.setheading(-unit.heading())
		if unit.ycor() > 50:
			unit.goto(unit.xcor(), 50)
			unit.setheading(-unit.heading())
