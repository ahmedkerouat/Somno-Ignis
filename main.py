import pygame as py
import random
import sys
from entity import Enemy
from entity import Player
from entity import Bed


# constants

WIDTH = 800
HEIGHT = 800
FPS = 60

WHITE = 255, 255, 255
BLACK = 0, 0, 0

POSTIONS1 = [(-100, -30), (830, 850)]
POSITIONS2 = (0, 800)
RANDOM_LIST = [POSTIONS1, POSITIONS2]

# initializing pygame

py.init()

window = py.display.set_mode([WIDTH, HEIGHT])
py.mouse.set_visible(False)
py.display.set_caption("Somno Ignis")

clock = py.time.Clock()
main_font = py.font.Font(
    "ressources\mainfont.ttf", 16)
program_icon = py.image.load("ressources\sprites\\bed.png")
py.display.set_icon(program_icon)


# Player


player1 = Player(200, 400, 1, 3)
enemies = []
bed = Bed(393, 383, 3)
update = py.time.get_ticks()

# Controls


def game_input(last_update, last_update_fire):
    keys = py.key.get_pressed()

    player1.idle == True
    player1.run = False

    if player1.idle == True:
        if player1.energy < 100:
            player1.energy += 0.1
        if 50 < player1.energy < 99:
            player1.energy *= 1.001

    player1.collision(bed)

    if player1.energy > 0 and player1.attack == False and player1.shoot == False:

        if keys[py.K_d] and player1.x < WIDTH - player1.width and player1.right_move:
            player1.flip = False
            player1.d_x = 1
            player1.x += 1 * player1.speed
            player1.idle = False
            player1.run = True
            player1.energy -= 0.08

        if keys[py.K_q] and player1.x > player1.width - 10 and player1.left_move:
            player1.flip = True
            player1.d_x = -1
            player1.x -= 1 * player1.speed
            player1.idle = False
            player1.run = True
            player1.energy -= 0.08

        if keys[py.K_s] and player1.y < HEIGHT - player1.height and player1.down_move:
            player1.y += 1 * player1.speed
            player1.d_y = -1
            player1.idle = False
            player1.run = True
            player1.energy -= 0.08

        if keys[py.K_z] and player1.y > player1.height and player1.up_move:
            player1.y -= 1 * player1.speed
            player1.d_y = 1
            player1.idle = False
            player1.run = True
            player1.energy -= 0.08

    if player1.attack == True and py.time.get_ticks() - last_update >= 4 * player1.latency:
        last_update = py.time.get_ticks()
        player1.attack = False
        player1.idle = True

    if player1.shoot == True and py.time.get_ticks() - last_update_fire >= 4 * player1.latency:
        last_update_fire = py.time.get_ticks()
        player1.shoot = False
        player1.idle = True


# rendering the game
points = 0


def game_render():
    # window.blit(bg, (0,0))
    window.fill((50, 50, 50))
    global points
    points = points + 0.01
    points_render = main_font.render(f"Points : {round(points)}", 1, WHITE)
    bed.draw(window)

    if len(enemies) < round(1 + points//50) < 20:
        global update
        if py.time.get_ticks() - update >= (points * (3000//(2 * points + 1))):
            rng = random.choice(RANDOM_LIST)
            if rng == POSTIONS1:
                rng = random.choice(POSTIONS1)
                u, v = rng
                w, c = POSITIONS2
            else:
                rng = random.choice(POSTIONS1)
                w, c = rng
                u, v = POSITIONS2

            dog = Enemy(random.randint(u, v), random.randint(
                w, c), 1, random.uniform((1 + points//500), (2 + points//500)))
            enemies.append(dog)
            update = py.time.get_ticks()

    for enemy in enemies:

        enemy.draw(window)

        def dead():
            enemy.alive = False
            enemy.dead_time = py.time.get_ticks()

        for bullet in player1.bullets:
            if bullet.rect.colliderect(enemy):
                dead()

        if enemy.alive:
            enemy.collision(bed)
            if enemy.collide == False:
                enemy.movement()
        elif enemy.frame_index == 5 and py.time.get_ticks() - enemy.dead_time >= 120:
            points += 10
            enemies.remove(enemy)

    for bullet in player1.bullets:
        bullet.display(window)
        if bullet.x > 800:
            player1.bullets.remove(bullet)
        if bullet.x < 0:
            player1.bullets.remove(bullet)

    for explosion in player1.explosions:
        explosion.animation()
        explosion.display(window)
        if explosion.end:
            player1.explosions.remove(explosion)
    player1.draw(window)
    player1.energy_status(window, main_font)
    window.blit(points_render, (10, 10))
    # other things to blit.
    py.display.update()

# main


def main():
    run = True
    last_update = py.time.get_ticks()
    last_update_fire = py.time.get_ticks()

    while run:
        clock.tick(FPS)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                sys.exit()

            if event.type == py.KEYUP:
                if event.key == py.K_a and player1.energy > 3:
                    if py.time.get_ticks() - last_update > 300:
                        bed_points = [bed.rect.midleft, bed.rect.midright]
                        for bed_point in bed_points:
                            if player1.rect.collidepoint(bed_point) and player1.energy > 33:
                                player1.x += 100 * player1.d_x
                                player1.tricks += 1
                                player1.explosion_effect()
                                player1.energy -= 30
                        player1.attack = True
                        player1.energy -= 3
                        last_update = py.time.get_ticks()

                if event.key == py.K_SPACE and player1.energy > 15:
                    if py.time.get_ticks() - last_update_fire > 300:
                        player1.shoot = True
                        player1.fireball()
                        player1.energy -= 15
                        last_update_fire = py.time.get_ticks()

        game_input(last_update, last_update_fire)
        game_render()


if __name__ == "__main__":
    main()
