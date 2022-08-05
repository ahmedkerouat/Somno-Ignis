import pygame as py
import sys
from entity import Player


# constants

WIDTH = 800
HEIGHT = 800
FPS = 60

WHITE = 255, 255, 255
BLACK = 0, 0, 0

# initializing pygame

py.init()

window = py.display.set_mode([WIDTH, HEIGHT])
py.display.set_caption("Game Test")

clock = py.time.Clock()
main_font = py.font.Font(
    "ressources\mainfont.ttf", 16)

# Player


player1 = Player(400, 400, 1, 3)

# Controls


def game_input():
    keys = py.key.get_pressed()
    player1.idle = True
    player1.run = False
    player1.attack = False
    player1.shoot = False

    if player1.idle == True:
        if player1.energy < 100:
            player1.energy += 0.1
        if 50 < player1.energy < 99:
            player1.energy *= 1.005

    if player1.idle == False:
        last_update = py.time.get_ticks()

    if player1.energy > 10:

        if keys[py.K_SPACE]:

            player1.idle = False
            player1.attack = True
            player1.energy -= 1.5

        if player1.energy > 40:

            if keys[py.K_a]:

                player1.idle = False
                player1.shoot = True
                player1.energy -= 2

        if keys[py.K_d] and player1.x < WIDTH - player1.width // 3:
            player1.flip = False
            player1.x += 1 * player1.speed
            player1.idle = False
            player1.run = True
            player1.energy -= 0.08

        if keys[py.K_q] and player1.x > player1.width // 3:
            player1.flip = True
            player1.x -= 1 * player1.speed
            player1.idle = False
            player1.run = True
            player1.energy -= 0.08

        if keys[py.K_s] and player1.y < HEIGHT - player1.height:
            player1.y += 1 * player1.speed
            player1.idle = False
            player1.run = True
            player1.energy -= 0.08

        if keys[py.K_z] and player1.y > player1.height // 3:
            player1.y -= 1 * player1.speed
            player1.idle = False
            player1.run = True
            player1.energy -= 0.08


# rendering the game
points = 0


def game_render():
    # window.blit(bg, (0,0))
    window.fill((50, 50, 50))
    points_render = main_font.render(f"Points : {points}", 1, WHITE)
    player1.draw(window)
    player1.energy_status(window, main_font)
    window.blit(points_render, (10, 10))
    # other things to blit.
    py.display.update()

# main


def main():
    run = True
    while run:
        clock.tick(FPS)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                sys.exit()
        game_input()
        game_render()


if __name__ == "__main__":
    main()
