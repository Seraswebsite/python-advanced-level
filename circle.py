import turtle

pen = turtle.Turtle()
pen.speed(5)
pen.color("red")

# Petals
for x in range(6):
    pen.circle(100, 60)
    pen.left(120)
    pen.circle(100, 60)
    pen.left(60)

# Flower center
pen.color("yellow")
pen.begin_fill()
pen.circle(30)
pen.end_fill()

# Stem
pen.penup()
pen.goto(0, -30)
pen.setheading(270)
pen.pendown()
pen.color("green")
pen.forward(200)

pen.hideturtle()

turtle.done()