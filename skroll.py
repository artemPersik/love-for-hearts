import pygame
import sys
import os

ind = 0
ideal = set()


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


CHARACTERS = ['алкаголик', 'жадина', 'злобный', 'раздрожительный', 'высокаомерный', 'лицимер', 'эгоистичен',
              'жесток', "ленивый", 'жизнерадостный', 'реалист', 'ЗОЖник', 'щедрый', 'добрый', 'спокойный', 'скромный',
              'прямолинейный', 'заботливый', 'добрый',
              "активный"]

BUTTONS_PASSIVE = {"0": load_image("alco.png", "/buttons"),
                   "1": load_image("jadina.png", "/buttons"),
                   "2": load_image("angry.png", "/buttons"),
                   "3": load_image("hfzdroj.png", "/buttons"),
                   "4": load_image("vsokmer.png", "/buttons"),
                   "5": load_image("licemer.png", "/buttons"),
                   "6": load_image("egoist.png", "/buttons"),
                   "7": load_image("jestok.png", "/buttons"),
                   "8": load_image("layzy.png", "/buttons"),
                   "9": load_image("jiznerad.png", "/buttons"),
                   "10": load_image("real.png", "/buttons"),
                   "11": load_image("zoj.png", "/buttons"),
                   "12": load_image("sedry.png", "/buttons"),
                   "13": load_image("dobry.png", "/buttons"),
                   "14": load_image("spokoiny.png", "/buttons"),
                   "15": load_image("skromn.png", "/buttons"),
                   "16": load_image("pryamolin.png", "/buttons"),
                   "17": load_image("zabot.png", "/buttons"),
                   "18": load_image("dobry.png", "/buttons"),
                   "19": load_image("active.png", "/buttons")}

BUTTONS_ACTIVE = {"0": load_image("alco2.png", "/buttons"),
                  "1": load_image("jadina2.png", "/buttons"),
                  "2": load_image("angry2.png", "/buttons"),
                  "3": load_image("hfzdroj2.png", "/buttons"),
                  "4": load_image("vsokmer2.png", "/buttons"),
                  "5": load_image("licemer2.png", "/buttons"),
                  "6": load_image("egoist2.png", "/buttons"),
                  "7": load_image("jestok2.png", "/buttons"),
                  "8": load_image("layzy2.png", "/buttons"),
                  "9": load_image("jiznerad2.png", "/buttons"),
                  "10": load_image("real2.png", "/buttons"),
                  "11": load_image("zoj2.png", "/buttons"),
                  "12": load_image("sedry2.png", "/buttons"),
                  "13": load_image("dobry2.png", "/buttons"),
                  "14": load_image("spokoiny2.png", "/buttons"),
                  "15": load_image("skromn2.png", "/buttons"),
                  "16": load_image("pryamolin2.png", "/buttons"),
                  "17": load_image("zabot2.png", "/buttons"),
                  "18": load_image("dobry2.png", "/buttons"),
                  "19": load_image("active2.png", "/buttons")}


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

ideal1 = Button(70, 65, 400, 100, BUTTONS_PASSIVE[str(ind)], BUTTONS_ACTIVE[str(ind)], BUTTONS_ACTIVE[str(ind)],
                lambda x=CHARACTERS[ind]: ideal.add(x))
ideal2 = Button(70, 215, 400, 100, BUTTONS_PASSIVE[str(ind + 1)], BUTTONS_ACTIVE[str(ind + 1)],
                BUTTONS_ACTIVE[str(ind + 1)], lambda x=CHARACTERS[ind + 1]: ideal.add(x))
ideal3 = Button(70, 365, 400, 100, BUTTONS_PASSIVE[str(ind + 2)], BUTTONS_ACTIVE[str(ind + 2)],
                BUTTONS_ACTIVE[str(ind + 2)], lambda x=CHARACTERS[ind + 2]: ideal.add(x))
ideal4 = Button(70, 515, 400, 100, BUTTONS_PASSIVE[str(ind + 3)], BUTTONS_ACTIVE[str(ind + 3)],
                BUTTONS_ACTIVE[str(ind + 3)], lambda x=CHARACTERS[ind + 3]: ideal.add(x))
ideal5 = Button(70, 665, 400, 100, BUTTONS_PASSIVE[str(ind + 4)], BUTTONS_ACTIVE[str(ind + 4)],
                BUTTONS_ACTIVE[str(ind + 4)], lambda x=CHARACTERS[ind + 4]: ideal.add(x))


class Scroll1:
    def __init__(self, x1, y1, x2, y2):
        global ind
        global ideal1, ideal2, ideal3, ideal4, ideal5
        mouse = pygame.mouse.get_pos()
        if x1 < mouse[0] < x2 and y1 < mouse[1] < y2:
            if event.button == 4:
                ind -= 1
                if ind < 0:
                    ind = 0
            elif event.button == 5:
                ind += 1
                if ind > len(CHARACTERS) - 5:
                    ind = len(CHARACTERS) - 5

            ideal1.kill()
            ideal2.kill()
            ideal3.kill()
            ideal4.kill()
            ideal5.kill()

            ideal1 = Button(x1, y1, 400, 100, BUTTONS_PASSIVE[str(ind)], BUTTONS_ACTIVE[str(ind)],
                            BUTTONS_ACTIVE[str(ind)],
                            lambda x=CHARACTERS[ind]: ideal.add(x))
            ideal2 = Button(70, y1 + 150, 400, 100, BUTTONS_PASSIVE[str(ind + 1)], BUTTONS_ACTIVE[str(ind + 1)],
                            BUTTONS_ACTIVE[str(ind + 1)], lambda x=CHARACTERS[ind + 1]: ideal.add(x))
            ideal3 = Button(70, y1 + 300, 400, 100, BUTTONS_PASSIVE[str(ind + 2)], BUTTONS_ACTIVE[str(ind + 2)],
                            BUTTONS_ACTIVE[str(ind + 2)], lambda x=CHARACTERS[ind + 2]: ideal.add(x))
            ideal4 = Button(70, y1 + 450, 400, 100, BUTTONS_PASSIVE[str(ind + 3)], BUTTONS_ACTIVE[str(ind + 3)],
                            BUTTONS_ACTIVE[str(ind + 3)], lambda x=CHARACTERS[ind + 3]: ideal.add(x))
            ideal5 = Button(70, y1 + 600, 400, 100, BUTTONS_PASSIVE[str(ind + 4)], BUTTONS_ACTIVE[str(ind + 4)],
                            BUTTONS_ACTIVE[str(ind + 4)], lambda x=CHARACTERS[ind + 4]: ideal.add(x))


cursor = Cursor()

clock = pygame.time.Clock()
FPS = 60
running = True
pygame.mouse.set_visible(False)

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            Scroll1(1, 1, 1, 1)
        button_group.update(event)
    screen.fill(pygame.Color("#DF1479"))
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(FPS)
    pygame.display.flip()
    print(ideal)

