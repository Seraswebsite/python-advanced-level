import turtle
import math
import random
import time

screen = turtle.Screen()
screen.setup(900, 900)
screen.bgcolor("black")
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)


def petal(size, angle, color):
    t.color(color)
    t.begin_fill()

    for x in range(2):
        t.circle(size, angle)
        t.left(180 - angle)

    t.end_fill()



for layer in range(5):

    size = 180 - layer * 25
    petals = 18 + layer * 6

    for x in range(petals):

        t.penup()
        t.goto(0, 0)
        t.setheading(x * (360 / petals))
        t.forward(20 + layer * 5)
        t.pendown()

        petal(size, 60, "purple")

        screen.update()



t.penup()
t.goto(0, -35)
t.setheading(0)
t.pendown()

t.color("yellow")
t.begin_fill()
t.circle(35)
t.end_fill()


particles = []

for x in range(80):

    p = turtle.Turtle()
    p.hideturtle()
    p.speed(0)

    angle = random.randint(0, 359)
    distance = random.randint(180, 400)

    px = math.cos(math.radians(angle)) * distance
    py = math.sin(math.radians(angle)) * distance

    p.penup()
    p.goto(px, py)
    p.dot(random.randint(2, 6), "cyan")

    particles.append(p)


angle = 0

while True:

    t.clear()

    # Outer petals
    for x in range(36):

        t.penup()
        t.goto(0, 0)

        t.setheading(x * 10 + angle)

        t.forward(30)
        t.pendown()

        petal(150, 60, "magenta")

  
    for x in range(24):

        t.penup()
        t.goto(0, 0)

        t.setheading(x * 15 - angle)

        t.forward(20)
        t.pendown()

        petal(90, 60, "purple")

    # Center
    t.penup()
    t.goto(0, -30)
    t.pendown()

    t.color("yellow")
    t.begin_fill()
    t.circle(30)
    t.end_fill()

    angle += 2

    screen.update()
    time.sleep(0.03)