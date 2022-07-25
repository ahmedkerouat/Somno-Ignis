import pygame as py
import sys

py.init()

WIDTH = 800
HEIGHT = 800
WHITE = 255, 255, 255
BLACK = 0, 0, 0

Rect_x = 40
Rect_y = 70

# used to center the position of the player on the start
Player_x = WIDTH / 2 - Rect_x / 2
Player_y = HEIGHT / 2 - Rect_y / 2

# Variable used to know if the cooldown is on.
cooldown_status = 0

# variables used for delay for certain actions
cooldown_time = 3000
delay_time = 1000

window = py.display.set_mode([WIDTH, HEIGHT])

run = True
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()

        if event.type == py.KEYDOWN:
            if event.key == py.K_a:
                now = py.time.get_ticks()
                if cooldown_status == 0:

                    activation_start = py.time.get_ticks()
                    activation_status = True
                    Player_x -= Rect_x/2
                    Player_y -= Rect_y/2
                    Rect_x *= 2
                    Rect_y *= 2

                    last = py.time.get_ticks()
                    cooldown_status = 1

                elif last + cooldown_time < now:
                    cooldown_status = 0

    window.fill(WHITE)
    py.draw.rect(window, BLACK, py.Rect(Player_x, Player_y, Rect_x, Rect_y))

# this portion of code verifies that the player will get back to normal, after a delay.

    if cooldown_status == 1:
        activation_timer = py.time.get_ticks()
        if activation_start + delay_time < activation_timer:
            if activation_status == True:

                Rect_x /= 2
                Rect_y /= 2
                Player_x += Rect_x/2
                Player_y += Rect_y/2

                activation_status = False

# Basic player movement
    keys = py.key.get_pressed()
    if keys[py.K_d]:
        Player_x += 0.1
        if int(Player_x) == 800:
            Player_x = 0

    if keys[py.K_q]:
        Player_x -= 0.1
        if int(Player_x) == 0:
            Player_x = 800

    if keys[py.K_s]:
        Player_y += 0.1
        if int(Player_y) == 800:
            Player_y = 0

    if keys[py.K_z]:
        Player_y -= 0.1
        if int(Player_y) == 0:
            Player_y = 800

    py.display.flip()
