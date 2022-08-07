import pygame as py


class SpriteSheet():
    def __init__(self, img):
        self.sheet = img

    def get_image(self, frame, animation, width, height, scale, colour):
        '''
        Method Used to extract a portion of a spritesheet.
        The method also scales up/down the sprite.
        We can then simply use the sprite for our need.
        '''

        img = py.Surface((width, height))
        img.blit(self.sheet, (0, 0), ((frame * width),
                 (width * animation), width, height))
        img = py.transform.scale(img, (width * scale, height * scale))
        img.set_colorkey(colour)  # for the transparency.

        return img


class Player(py.sprite.Sprite):

    def __init__(self, x, y, scale, speed):

        self.x = x
        self.y = y
        self.height = 48
        self.width = 50
        self.scale = scale
        self.speed = speed
        self.flip = False
        self.idle = True
        self.run = False
        self.attack = False
        self.shoot = False
        self.energy = 100
        self.frame_index = 0
        self.latency = 50

        py.sprite.Sprite.__init__(self)

        sprite_sheet_image_player = py.image.load(
            'ressources\sprites\characters\player_fire.png').convert_alpha()
        self.sprite_sheet_player = SpriteSheet(sprite_sheet_image_player)
        self.img_player = self.sprite_sheet_player.get_image(
            0, 0, self.height, self.width, 3, (0, 0, 0), )

        self.image = py.transform.scale(
            self.img_player, (int(self.img_player.get_width() * self.scale), int(self.img_player.get_height() * self.scale)))

        self.last_update = py.time.get_ticks()
        self.last_shot = py.time.get_ticks()

    def energy_status(self, surface, font):

        py.draw.rect(surface, (80, 80, 200), py.Rect(
            10, 770, (self.energy * 2), 18), 0, 3)
        py.draw.rect(surface, (80, 80, 200), py.Rect(
            10, 770, (100 * 2), 18), 2, 3)
        energy_render = font.render(
            f"Energy : {round(self.energy) } %", 1, (255, 255, 255))

        surface.blit(energy_render,
                     (60, 772))

    def animate(self, animation, max_frame):

        # Method used for creating animation, depending on the player input.

        if py.time.get_ticks() - self.last_update >= self.latency:
            img_player = self.sprite_sheet_player.get_image(
                self.frame_index, animation, self.height, self.width, 3, (0, 0, 0))
            self.image = py.transform.scale(
                img_player, (int(img_player.get_width() * self.scale), int(img_player.get_height() * self.scale)))
            self.frame_index += 1
            self.last_update = py.time.get_ticks()

        if self.frame_index > max_frame:
            self.frame_index = 0

    def draw(self, surface):

        # Method used for displaying the Player on the screen.

        if self.idle == True:
            self.animate(0, 5)

        if self.run == True:
            self.animate(1, 5)

        if self.attack == True:
            self.animate(2, 3)

        if self.shoot == True:
            self.current_update = py.time.get_ticks()
            if self.current_update - self.last_shot > 100 :
                self.animate(3, 3)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(py.transform.flip(
            self.image, self.flip, False), self.rect)


class Bed(py.sprite.Sprite):

    '''
    If the bed is broken, the game ends. The player can respawn if the bed is still not broken.
    '''

    def __init__(self, x, y, scale):

        self.x = x
        self.y = y
        self.scale = scale

    def is_broken():

        pass

    def draw():

        # Method used for displaying the bed on the screen.
        pass


class Bullet(py.sprite.Sprite):

    def __init__(self, x, y, direction):
        pass
