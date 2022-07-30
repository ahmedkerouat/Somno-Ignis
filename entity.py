import pygame as py


class SpriteSheet():
    def __init__(self, img):
        self.sheet = img

    def get_image(self, frame, width, height, scale, colour):
        img = py.Surface((width, height))
        img.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        img = py.transform.scale(img, (width * scale, height * scale))
        img.set_colorkey(colour)

        return img
