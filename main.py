import pygame
import sys
import os


def load_image(name, path='', colorkey=None):
    fullname = os.path.join(f'data/images{path}', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw_image(name, X, Y, path="", colorkey=None):
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image(name, path, colorkey)
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)
    sprite.rect.x = X
    sprite.rect.y = Y
    all_sprites.draw(screen)


class Cursor(pygame.sprite.Sprite):
    def __init__(self, image=None):
        super().__init__(all_sprites)
        self.image = cursor_image
        self.rect = self.image.get_rect()

    def update(self):
        if pygame.mouse.get_focused():
            self.rect.x, self.rect.y = pygame.mouse.get_pos()


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height, pass_image, direct_image, clicked_image, func):
        super().__init__(button_group, all_sprites)

        self.pass_image = pygame.transform.scale(load_image(pass_image), (width, height))
        self.direct_image = pygame.transform.scale(load_image(direct_image), (width, height))
        self.clicked_image = pygame.transform.scale(load_image(clicked_image), (width, height))
        self.image = self.pass_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = (pos_x, pos_y)
        self.func = func
        self.width, self.height = width, height

    def update(self, *events):
        if events and self.is_mouse_button_up(events[0]):
            self.image = self.clicked_image
            self.func()
        elif self.is_mouse_button_down():
            self.image = self.clicked_image
        elif self.is_direct():
            self.image = self.direct_image
        else:
            self.image = self.pass_image

    def is_direct(self):
        return not pygame.mouse.get_pressed(3)[0] and pygame.sprite.collide_mask(self, cursor)

    def is_mouse_button_down(self):
        return pygame.mouse.get_pressed(3)[0] and pygame.sprite.collide_mask(self, cursor)

    def is_mouse_button_up(self, event):
        return event.type == pygame.MOUSEBUTTONUP and event.button == 1 and pygame.sprite.collide_mask(self, cursor)

    def get_pos(self):
        return self.pos

    def get_pos_x(self):
        return self.pos[0]

    def get_pos_y(self):
        return self.pos[1]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_func(self):
        return self.func

    def set_pass_image(self, image):
        self.pass_image = load_image(image)

    def set_direct_image(self, image):
        self.direct_image = load_image(image)

    def set_clicked_image(self, image):
        self.clicked_image = load_image(image)

    def set_pos(self, pox_x, pos_y):
        self.pos = (pox_x, pos_y)
        self.rect.x, self.rect.y = self.get_pos()

    def set_width(self, width):
        self.width = width
        self.rect.width = self.get_width()

    def set_height(self, height):
        self.height = height
        self.rect.height = self.get_height()

    def set_func(self, func):
        self.func = func


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


pygame.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
all_sprites = pygame.sprite.Group()
button_group = pygame.sprite.Group()

cursor_image = load_image('cursor.png')
para = load_image("para2.png")

new_game_b = Button(70, 65, 600, 150, "new game.png", "new game2.png", "new game2.png", quit)
continue_b = Button(70, 265, 600, 150, "continue.png", "continue2.png", "continue2.png", quit)
options_b = Button(70, 465, 600, 150, "options.png", "options2.png", "options2.png", quit)
authors_b = Button(70, 665, 600, 150, "authors.png", "authors2.png", "authors2.png", quit)
quit_b = Button(70, 865, 600, 150, "quit.png", "quit2.png", "quit2.png", quit)
heart = AnimatedSprite(load_image("heart.png"), 6, 2, 1100, 53)

cursor = Cursor()

clock = pygame.time.Clock()
FPS = 60
running = True
pygame.mouse.set_visible(False)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button_group.update(event)
    screen.fill(pygame.Color("#DF1479"))
    draw_image("para2.png", 900, 53)
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(FPS)
    pygame.display.flip()
