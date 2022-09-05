import pygame as py


class Interface():

    def __init__(self, font, highscore, highscore_font):
        self.font = font
        self.highscore = highscore
        self.highscore_font = highscore_font
        self.mx = 0
        self.my = 0
        self.clicked1 = False
        self.clicked2 = False
        self.clicked3 = False
        self.clicked_github = False
        self.color1 = (20, 0, 46)
        self.color2 = (20, 0, 46)
        self.color3 = (20, 0, 46)
        self.menu_bg = py.image.load("ressources\sprites\\menu_bg.png")
        logo_unscaled = py.image.load("ressources\sprites\\gamelogo.png")
        self.logo = py.transform.scale(logo_unscaled, (int(
            logo_unscaled.get_width() * 3), int(logo_unscaled.get_height() * 3)))
        self.last_update = py.time.get_ticks()

        github_unscaled = py.image.load(
            f"ressources\sprites\\github0.png")
        self.logo_github = py.transform.scale(github_unscaled, (int(
            github_unscaled.get_width() * 2), int(github_unscaled.get_height() * 2)))
        self.logo_github_rect = self.logo_github.get_rect()
        self.logo_github_rect.center = (38, 768)

    def update_highscore(self, highscore):
        self.highscore_render = self.highscore_font.render(
            ("Highscore : " + str(self.highscore)), 1, (200, 100, 0))
        self.highscore_width = self.highscore_render.get_width()
        self.highscore = highscore

    def display(self, surface):
        self.mx, self.my = py.mouse.get_pos()
        py.mouse.set_visible(True)
        surface.blit(self.menu_bg, (0, 0))
        surface.blit(self.logo, (200, 0))
        button = Button(367, 300, "play", self.font,
                        self.color1,  self.mx, self.my)
        button.display(surface)
        if button.button1_rect.collidepoint(self.mx, self.my):
            self.color1 = (200, 100, 0)
            if py.mouse.get_pressed()[0]:
                self.clicked1 = True
        else:
            self.color1 = (20, 0, 46)

        button2 = Button(367, 400, "quit", self.font,
                         self.color2,  self.mx, self.my)
        button2.display(surface)
        if button2.button1_rect.collidepoint(self.mx, self.my):
            self.color2 = (200, 100, 0)
            if py.mouse.get_pressed()[0]:
                self.clicked2 = True
        else:
            self.color2 = (20, 0, 46)
        surface.blit(self.highscore_render,
                     (400 - (self.highscore_width // 2), 125))

        button3 = Button(345, 350, "options", self.font,
                         self.color3, self.mx, self.my)
        button3.display(surface)
        if button3.button1_rect.collidepoint(self.mx, self.my):
            self.color3 = (200, 100, 0)
            if py.mouse.get_pressed()[0]:
                self.clicked3 = True
        else:
            self.color3 = (20, 0, 46)

        surface.blit(self.logo_github, (5, 735))
        if self.logo_github_rect.collidepoint(self.mx, self.my):
            if py.mouse.get_pressed()[0]:
                self.clicked_github = True
            github_unscaled = py.image.load(
                f"ressources\sprites\\github1.png")
            self.logo_github = py.transform.scale(github_unscaled, (int(
                github_unscaled.get_width() * 2), int(github_unscaled.get_height() * 2)))
        else:
            self.clicked_github = False
            github_unscaled = py.image.load(
                f"ressources\sprites\\github0.png")
        self.logo_github = py.transform.scale(github_unscaled, (int(
            github_unscaled.get_width() * 2), int(github_unscaled.get_height() * 2)))


class Button():

    def __init__(self, x, y, text, font, color, mx, my):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.mx = mx
        self.my = my

    def display(self, surface):
        self.button1 = self.font.render(self.text, 1, self.color)
        self.button1_rect = self.button1.get_rect()
        self.button1_rect.center = (self.x + 30, self.y + 12)
        surface.blit(self.button1, (self.x, self.y))
