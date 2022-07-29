import pygame as py
from main import *


class Player(py.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        py.sprite.Sprite.__init__(self)
        self.speed = speed
        img_player = ""
        self.image = py.transform.scale(
            img_player, (int(img_player.get_width() * scale), int(img_player.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        window.blit(self.image, self.rect)
