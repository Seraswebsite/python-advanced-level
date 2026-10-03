import turtle
import random
import math

# -----------------------------
# SCREEN SETUP
# -----------------------------
screen = turtle.Screen()
screen.setup(1000, 700)
screen.bgcolor("black")
screen.title("✨ Neon Galaxy Portal ✨")
screen.tracer(0)

# -----------------------------
# MAIN TURTLE
# -----------------------------
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

# -----------------------------
# CREATE STARS
# -----------------------------
stars = []

for x in range(120):
    star = turtle.Turtle()
    star.shape("circle")
    star.color(random.choice(["white", "cyan", "light blue"]))
    star.penup()

    star.goto(
        random.randint(-480, 480),
        random.randint(-330, 330)
    )

    size = random.choice([0.05, 0.08, 0.12])
    star.shapesize(size, size)

    stars.append(star)

# -----------------------------
# CREATE PARTICLES
# -----------------------------
particles = []

for x in range(60):
    particle = turtle.Turtle()
    particle.shape("circle")
    particle.color(random.choice([
        "cyan",
        "blue",
        "magenta",
        "purple",
        "white"
    ]))

    particle.penup()

    angle = random.uniform(0, math.pi * 2)
    distance = random.randint(80, 280)

    particle.goto(
        math.cos(angle) * distance,
        math.sin(angle) * distance
    )

    particle.speed(0)
    particle.shapesize(0.08, 0.08)

    particles.append(particle)

# -----------------------------
# DRAW ROTATING RING
# -----------------------------
rings = []

for radius in [70, 110, 150, 190, 230]:

    ring = turtle.Turtle()
    ring.hideturtle()
    ring.speed(0)
    ring.penup()

    rings.append((ring, radius))

# -----------------------------
# DRAW RING FUNCTION
# -----------------------------
def draw_ring(t, radius, rotation):

    t.clear()
    t.penup()

    for angle in range(0, 360, 8):

        a = math.radians(angle + rotation)

        x = math.cos(a) * radius
        y = math.sin(a) * radius

        if angle % 16 == 0:
            t.goto(x, y)
            t.pendown()

            t.dot(3, "cyan")

            t.penup()

# -----------------------------
# GALAXY SPIRAL
# -----------------------------
galaxy = turtle.Turtle()
galaxy.hideturtle()
galaxy.speed(0)

# -----------------------------
# ANIMATION
# -----------------------------
rotation = 0
particle_angle = 0
pulse = 0

def animate():

    global rotation
    global particle_angle
    global pulse

    # -------------------------
    # ROTATE RINGS
    # -------------------------
    colors = [
        "cyan",
        "blue",
        "magenta",
        "purple",
        "cyan"
    ]

    for number, (ring, radius) in enumerate(rings):

        ring.color(colors[number])

        draw_ring(
            ring,
            radius,
            rotation * (number + 1)
        )

    # -------------------------
    # MOVE PARTICLES
    # -------------------------
    particle_angle += 2

    for number, particle in enumerate(particles):

        angle = math.radians(
            particle_angle + number * 6
        )

        distance = 100 + (
            number * 3
        )

        x = math.cos(angle) * distance
        y = math.sin(angle) * distance

        particle.goto(x, y)

    # -------------------------
    # GALAXY SPIRAL
    # -------------------------
    galaxy.clear()

    galaxy.penup()

    for angle in range(0, 720, 4):

        radians = math.radians(angle)

        distance = angle * 0.35

        x = math.cos(
            radians + rotation * 0.02
        ) * distance

        y = math.sin(
            radians + rotation * 0.02
        ) * distance

        galaxy.goto(x, y)

        galaxy.dot(
            2,
            random.choice([
                "cyan",
                "blue",
                "purple",
                "magenta"
            ])
        )

    # -------------------------
    # PULSING CENTER
    # -------------------------
    pulse += 4

    center_size = 10 + abs(
        math.sin(math.radians(pulse))
    ) * 18

    pen.clear()

    pen.penup()
    pen.goto(0, -center_size)

    pen.color("white")
    pen.begin_fill()
    pen.circle(center_size)
    pen.end_fill()

    # -------------------------
    # UPDATE
    # -------------------------
    rotation += 2

    screen.update()

    screen.ontimer(
        animate,
        30
    )

# -----------------------------
# START
# -----------------------------
animate()

turtle.done()