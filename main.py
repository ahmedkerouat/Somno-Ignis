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
ENEMY_TYPES = ["dog", "scorpio", "dog",
               "scorpio", "scorpio", "skeleton"]

# initializing pygame

py.init()

# requirements

window = py.display.set_mode([WIDTH, HEIGHT])
py.display.set_caption("Somno Ignis")

clock = py.time.Clock()
main_font = py.font.Font(
    "ressources\mainfont.ttf", 16)
font = py.font.Font(
    "ressources\mainfont.ttf", 32)
program_icon = py.image.load("ressources\sprites\\icon.png")
logo_unscaled = py.image.load("ressources\sprites\\gamelogo.png")
bg = py.image.load("ressources\sprites\\bg.png")
logo = py.transform.scale(logo_unscaled, (int(
    logo_unscaled.get_width() * 3), int(logo_unscaled.get_height() * 3)))
py.display.set_icon(program_icon)
click = False
points = 0

# Objects


player1 = Player(200, 400, 1, 3)
enemies = []
beds = []
bed1 = Bed(393, 383, 3)
beds.append(bed1)
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

def game_render():
    window.blit(bg, (0, 0))
    py.mouse.set_visible(False)
    global points
    points = points + 0.01
    points_render = main_font.render(f"Points : {round(points)}", 1, WHITE)
    player1.draw(window)

    if len(enemies) < round(1 + points//50) < 50:
        global update
        if py.time.get_ticks() - update >= (points * (3000//(2 * points + 1))):
            enemy_type = random.choice(ENEMY_TYPES)
            rng = random.choice(RANDOM_LIST)
            if rng == POSTIONS1:
                rng = random.choice(POSTIONS1)
                u, v = rng
                w, c = POSITIONS2
            else:
                rng = random.choice(POSTIONS1)
                w, c = rng
                u, v = POSITIONS2

            if enemy_type == "dog":
                dog = Enemy("dog", random.randint(u, v), random.randint(
                    w, c), 1, 30, 20, random.uniform((0.5 + points//400), (1 + points//400)), 100, 0, 0)
                enemies.append(dog)
            elif enemy_type == "scorpio":
                scorpio = Enemy("scorpio", random.randint(u, v), random.randint(
                    w, c), 1, 24, 19, random.uniform((0.5 + points//800), (1 + points//800)), 180, 2, 2)
                enemies.append(scorpio)
            elif enemy_type == "skeleton":
                scorpio = Enemy("skeleton", random.randint(u, v), random.randint(
                    w, c), 1, 25, 25, random.uniform((0.4 + points//700), (0.8 + points//700)), 220, 1, 2)
                enemies.append(scorpio)
            update = py.time.get_ticks()

    for enemy in enemies:

        enemy.draw(window)
        for bullet in player1.bullets:
            if bullet.rect.colliderect(enemy):
                enemy.hit = True
                enemy.life_points -= 35
                enemy.hit_time = py.time.get_ticks()

        for explosion in player1.explosions:
            if explosion.rect.colliderect(enemy):
                enemy.life_points -= 100
                enemy.hit = True
                enemy.hit_time = py.time.get_ticks()
                if enemy.life_points < 0:
                    enemy.dead()

        if py.time.get_ticks() - enemy.hit_time > 140 and enemy.hit == True:
            enemy.hit = False
            if enemy.life_points < 0:
                enemy.dead()

        if enemy.alive and enemy.hit == False:
            if player1.killable == False:
                for bed in beds:
                    enemy.collision(bed)
                    if enemy.attack == True:
                        bed.destruction_points += 0.1 + (points//1000)
                if enemy.collide == False:
                    enemy.movement(395, 420, 405, 410)
            else:
                enemy.collision(player1)
                if enemy.collide == True and enemy.attack == True and player1.life_points > 0:
                    player1.energy -= 0.1
                    player1.life_points -= 3 * (points/500)
                else:
                    enemy.movement(player1.x - 2, player1.x + 2,
                                   player1.y - 2, player1.y + 2)
        elif enemy.frame_index >= 5 - enemy.substract and py.time.get_ticks() - enemy.dead_time >= enemy.latency * (3 + enemy.substract):
            points += 10
            enemies.remove(enemy)
            for bed in beds:
                if bed.destruction_points > 0:
                    bed.destruction_points -= 1

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
    player1.energy_status(window, main_font)
    for bed in beds:
        player1.collision(bed)
        bed.draw(window, main_font)
        if bed.destruction_points >= 100:
            beds.remove(bed)
            player1.killable = True
    window.blit(points_render, (10, 10))
    if player1.life_points < 100 and player1.alive:
        player1.life_points_display(window, main_font)
    py.display.update()

# main


def main():
    run = True
    last_update = py.time.get_ticks()
    last_update_fire = py.time.get_ticks()

    while run:
        clock.tick(FPS)

        if player1.alive == False:
            py.mouse.set_visible(True)
            mx, my = py.mouse.get_pos()
            window.fill((11, 0, 19))
            window.blit(logo, (200, 0))
            button1 = font.render("PLAY", 1, WHITE)
            button1_rect = button1.get_rect()
            window.blit(button1, (374, 400))
            py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                sys.exit()

            if event.type == py.KEYUP and player1.alive:
                if event.key == py.K_a and player1.energy > 3:
                    if py.time.get_ticks() - last_update > 300:
                        for bed in beds:
                            bed_points = [bed.rect.midleft, bed.rect.midright]
                            for bed_point in bed_points:
                                if player1.rect.collidepoint(bed_point) and player1.energy > 33:
                                    player1.x += 100 * player1.d_x
                                    player1.tricks += 1
                                    player1.explosion_effect()
                                    player1.energy -= 30
                        player1.attack = True
                        for enemy in enemies:
                            if player1.rect.colliderect(enemy.rect) and player1.attack == True:
                                enemy.life_points -= 60
                                enemy.hit = True
                                enemy.hit_time = py.time.get_ticks()
                                if enemy.life_points < 0:
                                    enemy.dead()
                        player1.energy -= 3
                        last_update = py.time.get_ticks()

                if event.key == py.K_SPACE and player1.energy > 15:
                    if py.time.get_ticks() - last_update_fire > 300:
                        player1.shoot = True
                        player1.fireball()
                        player1.energy -= 15
                        last_update_fire = py.time.get_ticks()
        if player1.alive:
            game_input(last_update, last_update_fire)
            game_render()
            player1.check_if_dead()


if __name__ == "__main__":
    main()
