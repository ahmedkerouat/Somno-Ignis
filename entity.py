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
                 (height * animation), width, height))
        img = py.transform.scale(img, (width * scale, height * scale))
        img.set_colorkey(colour)  # for the transparency.

        return img


class Player(py.sprite.Sprite):

    def __init__(self, x, y, scale, speed):

        self.x = x
        self.y = y
        self.d_x = 0
        self.d_y = 0
        self.height = 22
        self.width = 22
        self.scale = scale
        self.speed = speed
        self.flip = False
        self.idle = True
        self.run = False
        self.collide = False
        self.attack = False
        self.shoot = False
        self.killable = False
        self.life_points = 100
        self.alive = True
        self.energy = 100
        self.bullets = []
        self.explosions = []
        self.frame_index = 0
        self.latency = 50
        self.cooldown_status = 0
        self.color_energy = 80, 80, 200
        self.down_move = True
        self.up_move = True
        self.left_move = True
        self.right_move = True
        self.tricks = 0

        py.sprite.Sprite.__init__(self)

        sprite_sheet_image_player = py.image.load(
            'ressources\sprites\characters\player.png').convert_alpha()
        self.sprite_sheet_player = SpriteSheet(sprite_sheet_image_player)
        self.img_player = self.sprite_sheet_player.get_image(
            0, 0, self.height, self.width, 3, (0, 0, 0), )

        self.image = py.transform.scale(
            self.img_player, (int(self.img_player.get_width() * self.scale), int(self.img_player.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.width *= 0.8
        self.rect.height *= 0.98

        self.last_update = py.time.get_ticks()
        self.dead_time = py.time.get_ticks()

    def energy_status(self, surface, font):

        py.draw.rect(surface, self.color_energy, py.Rect(
            10, 770, (self.energy * 2), 18), 0, 3)
        py.draw.rect(surface, self.color_energy, py.Rect(
            10, 770, (100 * 2), 18), 2, 3)
        energy_render = font.render(
            f"Energy : {round(self.energy) } %", 1, (255, 255, 255))

        if self.energy > 30:
            self.color_energy = 250, 160, 0

        if self.energy < 30:
            self.color_energy = 250, 105, 0

        if self.energy < 10:
            self.color_energy = 130, 10, 10

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

        if self.frame_index > max_frame and self.killable == False:
            self.frame_index = 0
        elif self.frame_index > max_frame and self.killable:
            self.frame_index = 2

    def fireball(self):
        bullet = Bullet(self.x, (self.y), self)
        self.bullets.append(bullet)

    def explosion_effect(self):
        self.explosion = Explosion(self.x, self.y)
        self.explosions.append(self.explosion)

    def check_if_dead(self):
        if self.killable:
            if self.frame_index >= 2 and py.time.get_ticks() - self.dead_time >= 600:
                self.alive = False

    def collision(self, obstacle):

        global down_move, up_move, left_move, right_move
        self.down_move = True
        self.up_move = True
        self.left_move = True
        self.right_move = True
        self.collide = False
        collision_tolerance = 10

        if self.rect.colliderect(obstacle):

            if abs(obstacle.rect.top - self.rect.bottom) < collision_tolerance:
                self.down_move = False
                self.collide = True
            if abs(obstacle.rect.bottom - self.rect.top) < collision_tolerance:
                self.up_move = False
                self.collide = True
            if abs(obstacle.rect.right - self.rect.left) < collision_tolerance:
                self.left_move = False
                self.collide = True
            if abs(obstacle.rect.left - self.rect.right) < collision_tolerance:
                self.right_move = False
                self.collide = True

    def draw(self, surface):

        # Method used for displaying the Player on the screen.

        if self.killable == False:

            if self.attack == True:
                self.idle = False
                self.animate(2, 3)

            if self.run == True:
                self.idle = False
                self.animate(1, 5)

            if self.shoot == True:
                self.idle = False
                self.animate(3, 3)

            else:
                self.idle = True
                self.animate(0, 5)
        else:
            self.animate(4, 2)

        self.rect.center = (self.x, self.y)
        surface.blit(py.transform.flip(
            self.image, self.flip, False), self.rect)


class Bed(py.sprite.Sprite):

    '''
    If the bed is broken, the player dies. 
    '''

    def __init__(self, x, y, scale):

        self.x = x
        self.y = y
        self.scale = scale
        self.destruction_points = 0
        self.broken = False
        self.img = py.image.load(
            "ressources\sprites\\bed.png").convert_alpha()
        self.image = py.transform.scale(
            self.img, (int(self.img.get_width() * self.scale), int(self.img.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.rect.w *= 0.9
        self.rect.h *= 0.9

    def is_broken(self):

        # Method used to check if the bed is broken or not

        if self.destruction_points >= 100:
            self.broken = True

    def draw(self, surface, font):

        # Method used for displaying the bed on the screen.

        if self.destruction_points > 0:
            py.draw.rect(surface, (130, 10, 10), py.Rect(
                590, 770, ((self.destruction_points) * 2), 18), 0, 3)
            py.draw.rect(surface, (130, 10, 10), py.Rect(
                590, 770, (100 * 2), 18), 2, 3)
            bed_status = font.render(
                f"Bed broken : {round(self.destruction_points) } %", 1, (255, 255, 255))
            surface.blit(bed_status,
                         (633, 772))
        surface.blit(py.transform.flip(
            self.image, False, False), self.rect)


class Bullet(py.sprite.Sprite):

    def __init__(self, x, y, player):

        if player.flip == True:
            self.direction = -1
            self.flip = True

        else:
            self.direction = 1
            self.flip = False

        self.speed = 10
        self.scale = 3
        self.x = x
        self.y = y
        self.img = py.image.load(
            "ressources\sprites\characters\\fireball.png").convert_alpha()
        self.image = py.transform.scale(
            self.img, (int(self.img.get_width() * self.scale), int(self.img.get_height() * self.scale)))
        self.rect = self.image.get_rect()

    def display(self, surface):
        self.x = self.x + (17 * self.direction)
        self.rect.center = (self.x, self.y)
        surface.blit(py.transform.flip(
            self.image, self.flip, False), self.rect)


class Explosion(py.sprite.Sprite):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.scale = 1
        self.height = self.width = 64
        self.latency = 15
        self.frame_index = 0
        self.animation_index = 0
        self.end = False
        self.last_update = py.time.get_ticks()

        sprite_sheet_image_explosion = py.image.load(
            'ressources\sprites\explosion.png').convert_alpha()
        self.sprite_sheet_explosion = SpriteSheet(sprite_sheet_image_explosion)
        self.img_explosion = self.sprite_sheet_explosion.get_image(
            0, 0, self.height, self.width, 3, (0, 0, 0), )
        self.image = py.transform.scale(
            self.img_explosion, (int(self.img_explosion.get_width() * self.scale), int(self.img_explosion.get_height() * self.scale)))
        self.rect = self.image.get_rect()

    def animation(self):
        if py.time.get_ticks() - self.last_update >= self.latency:
            img_explosion = self.sprite_sheet_explosion.get_image(
                self.frame_index, self.animation_index, self.height, self.width, 3, (0, 0, 0))
            self.image = py.transform.scale(
                img_explosion, (int(img_explosion.get_width() * self.scale), int(img_explosion.get_height() * self.scale)))
            self.frame_index += 1
            self.last_update = py.time.get_ticks()

        if self.frame_index > 3:
            self.frame_index = 0
            self.animation_index += 1
        if self.animation_index > 3:
            self.end = True

    def display(self, surface):
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        if self.end == False:
            surface.blit(py.transform.flip(
                self.image, False, False), self.rect)


class Enemy(py.sprite.Sprite):

    def __init__(self, name,  x, y, scale, height, width, speed, life_points, substract, add):
        self.x = x
        self.y = y
        self.scale = scale
        self.speed = speed
        self.alive = True
        self.move = False
        self.attack = False
        self.hit = False
        self.substract = substract
        self.add = add
        self.life_points = life_points
        self.height = height
        self.width = width
        self.flip = False
        self.frame_index = 0
        self.collide = False
        self.latency = 60
        self.dist1 = 0
        self.dist2 = 0
        sprite_sheet_image_enemy = py.image.load(
            "ressources\sprites\characters\\" + name + ".png").convert_alpha()
        self.sprite_sheet_enemy = SpriteSheet(sprite_sheet_image_enemy)
        self.img_enemy = self.sprite_sheet_enemy.get_image(
            0, 0, self.height, self.width, 3, (0, 0, 0), )
        self.image = py.transform.scale(
            self.img_enemy, (int(self.img_enemy.get_width() * self.scale), int(self.img_enemy.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.height *= 0.88
        self.rect.width *= 0.86
        self.last_update = py.time.get_ticks()
        self.hit_time = py.time.get_ticks()
        self.dead_time = py.time.get_ticks()

    def animate(self, animation, max_frame):

        if py.time.get_ticks() - self.last_update >= self.latency:
            img_enemy = self.sprite_sheet_enemy.get_image(
                self.frame_index, animation, self.height, self.width, 3, (0, 0, 0))
            self.image = py.transform.scale(
                img_enemy, (int(img_enemy.get_width() * self.scale), int(img_enemy.get_height() * self.scale)))
            self.frame_index += 1
            self.last_update = py.time.get_ticks()

        if self.frame_index > max_frame and self.alive == True:
            self.frame_index = 0
        if self.alive == False:
            self.frame_index = 5 - self.substract

    def collision(self, obstacle):
        collision_tolerance = 10

        if self.rect.colliderect(obstacle):

            self.collide = True

            if abs(obstacle.rect.top - self.rect.bottom) < collision_tolerance:
                self.move = True
                self.x += self.speed * 3
            if abs(obstacle.rect.bottom - self.rect.top) < collision_tolerance:
                self.move = True
                self.x -= self.speed * 3
            if abs(obstacle.rect.right - self.rect.left) < collision_tolerance:
                self.move = False
                self.attack = True
            if abs(obstacle.rect.left - self.rect.right) < collision_tolerance:
                self.move = False
                self.attack = True
        else:
            self.collide = False
            self.attack = False

    def dead(self):
        self.alive = False
        self.dead_time = py.time.get_ticks()

    def movement(self, x1, x2, y1, y2):

        if self.x < x1:
            self.x += self.speed
            self.flip = True
            self.move = True
            self.attack = False
        if self.x > x2:
            self.x -= self.speed
            self.flip = False
            self.move = True
            self.attack = False

        if self.y < y1:
            self.y += self.speed
            self.move = True
            self.attack = False
        if self.y > y2:
            self.y -= self.speed
            self.move = True
            self.attack = False

    def draw(self, surface):
        if self.hit == True:
            self.animate(4, 1)
        if self.alive and self.hit == False:
            if self.move == True:
                self.animate(1, 5 - self.substract)
            if self.attack == True:
                self.animate(2, 5 - self.add)

            else:
                self.animate(0, 3)
        else:
            self.animate(3, 5 - self.add)

        self.rect.center = (self.x, self.y)
        surface.blit(py.transform.flip(
            self.image, self.flip, False), self.rect)
