import pygame as py
import sys
from entity import *


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

move_left = False
move_right = False
# Player


class Player(py.sprite.Sprite):

    def __init__(self, x, y, scale, speed):

        self.x = x
        self.y = y
        self.scale = scale
        self.speed = speed
        self.flip = False

    def draw(self):
        sprite_sheet_image_player = py.image.load(
            'ressources\sprites\characters\player_fire.png').convert_alpha()
        sprite_sheet_player = SpriteSheet(sprite_sheet_image_player)
        py.sprite.Sprite.__init__(self)
        img_player = sprite_sheet_player.get_image(
            0, 50, 50, 3, (0, 0, 0), )
        self.image = py.transform.scale(
            img_player, (int(img_player.get_width() * self.scale), int(img_player.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        window.blit(py.transform.flip(
            self.image, self.flip, False), self.rect)


player1 = Player(400, 400, 1, 3)

# Controls


def game_input():
    keys = py.key.get_pressed()

    if keys[py.K_d]:
        player1.flip = False
        player1.x += 3

    if keys[py.K_q]:
        player1.flip = True
        player1.x -= 3
    if keys[py.K_s]:
        player1.y += 3

    if keys[py.K_z]:
        player1.y -= 3


# rendering the game


points = 0


def game_render():
    #window.blit(bg, (0,0))
    window.fill((50, 50, 50))
    points_render = main_font.render(f"Points : {points}", 1, WHITE)
    player1.draw()
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


main()
