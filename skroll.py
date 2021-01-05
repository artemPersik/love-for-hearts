import pygame
import sys
import os

CHARACTERS = ['алкаголик', 'жадина', 'злобный', 'раздрожительный', 'высокаомерный', 'лицимер', 'эгоистичен',
              'жесток', "ленивый", 'жизнерадостный', 'реалист', 'ЗОЖник', 'щедрый', 'добрый', 'спокойный', 'скромный',
              'прямолинейный', 'заботливый', 'добрый',
              "активный"]

#BUTTONS = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"]



ind = 0


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

BUTTONS = {"0": load_image("1.png"),
           "1": load_image("2.png"),
           "2": load_image("3.png"),
           "3": load_image("4.png"),
           "4": load_image("5.png"),
           "5": load_image("6.png"),
           "6": load_image("7.png")}

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

        self.pass_image = pygame.transform.scale(pass_image, (width, height))
        self.direct_image = pygame.transform.scale(direct_image, (width, height))
        self.clicked_image = pygame.transform.scale(clicked_image, (width, height))
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

    def __del__(self):
        pass

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
size = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
button_group = pygame.sprite.Group()

cursor_image = load_image('cursor.png')

"""new_game_b = Button(70, 65, 600, 150, "new game.png", "new game2.png", "new game2.png", quit)
continue_b = Button(70, 265, 600, 150, "continue.png", "continue2.png", "continue2.png", quit)
options_b = Button(70, 465, 600, 150, "options.png", "options2.png", "options2.png", quit)"""

new_game_b = Button(70, 65, 600, 150, BUTTONS[str(ind)], BUTTONS[str(ind)], BUTTONS[str(ind)], quit)
continue_b = Button(70, 265, 600, 150, BUTTONS[str(ind + 1)], BUTTONS[str(ind + 1)], BUTTONS[str(ind + 1)], quit)
options_b = Button(70, 465, 600, 150, BUTTONS[str(ind + 2)], BUTTONS[str(ind + 2)], BUTTONS[str(ind + 2)], quit)


def scroll():
    global ind
    global new_game_b
    global continue_b
    global options_b

    mouse = pygame.mouse.get_pos()
    if 70 < mouse[0] < 670 and 65 < mouse[1] < 615:
        if event.button == 4:
            ind -= 1
            if ind < 0:
                ind = 0
        elif event.button == 5:
            ind += 1
            if ind > len(BUTTONS) - 3:
                ind = len(BUTTONS) - 3

        del new_game_b, continue_b, options_b

        new_game_b = Button(70, 65, 600, 150, BUTTONS[str(ind)], BUTTONS[str(ind)], BUTTONS[str(ind)], quit)
        continue_b = Button(70, 265, 600, 150, BUTTONS[str(ind + 1)], BUTTONS[str(ind + 1)], BUTTONS[str(ind + 1)],quit)
        options_b = Button(70, 465, 600, 150, BUTTONS[str(ind + 2)], BUTTONS[str(ind + 2)], BUTTONS[str(ind + 2)], quit)



cursor = Cursor()

clock = pygame.time.Clock()
FPS = 60
running = True
pygame.mouse.set_visible(False)

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            scroll()
        button_group.update(event)
    screen.fill(pygame.Color("#DF1479"))
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(FPS)
    pygame.display.flip()