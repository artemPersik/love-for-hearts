import pygame
import sys
import os

CHARACTERS = ['алкаголик', 'жадина', 'злобный', 'раздрожительный', 'высокаомерный', 'лицимер', 'эгоистичен',
              'жесток', "ленивый", 'жизнерадостный', 'реалист', 'ЗОЖник', 'щедрый', 'добрый', 'спокойный', 'скромный',
              'прямолинейный', 'заботливый', 'добрый',
              "активный"]

ind = 0
ind2 = 0
flag = False
prom_age = ""
ideal = set()
you = set()
player = {}


def load_image(name, path='', colorkey=None):
    fullname = os.path.join(f'data/images{path}', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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

IMAGES = {"quit": load_image("quit.png", "/buttons"),
          "quit2": load_image("quit2.png", "/buttons"),
          "continue": load_image("continue.png", "/buttons"),
          "continue2": load_image("continue2.png", "/buttons"),
          }


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


class Spinbox:
    def __init__(self, x1, y1, x2, y2):
        global flag
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        global prom_age
        if (x1 < mouse[0] < x2 and y1 < mouse[1] < y2) and click[0]:
            flag = True
        elif ((x1 < mouse[0] or mouse[0] > x2) and (y1 < mouse[1] or mouse[0] > y2)) and click[0]:
            flag = False
        elif ((x1 > mouse[0] or mouse[0] < x2) and (y1 > mouse[1] or mouse[0] < y2)) and click[0]:
            flag = False

        if flag:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    prom_age = prom_age[0:-1]
                if len(prom_age) < 2:
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        prom_age += "9"
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        prom_age += "8"
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        prom_age += "7"
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        prom_age += "6"
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        prom_age += "5"
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        prom_age += "4"
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        prom_age += "3"
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        prom_age += "2"
                    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        prom_age += "1"
                    elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        prom_age += "0"


def render_description(screen, description, text_coord_x, text_coord_y):
    text = []
    line = ''

    for i, word in enumerate(description.split()):
        if len(line) + len(word) <= 40:
            line += f' {word}'
        else:
            text.append(line[1:])
            line = f' {word}'

        if i == len(description.split()) - 1:
            text.append(line[1:])

    font = pygame.font.Font(None, 35)
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord_y += 30
        intro_rect.top = text_coord_y
        intro_rect.x = text_coord_x
        text_coord_y += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def continue_b():
    global player
    player = {"gender": "W",
              "gender_partner": "M",
              "age": int(prom_age),
              "character": you,
              "character_partner": ideal}
    quit()


pygame.init()
pygame.font.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
# screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
button_group = pygame.sprite.Group()

cursor_image = load_image('cursor.png')
quit_b = Button(660, 860, 600, 150, IMAGES["continue"], IMAGES["continue2"], IMAGES["continue2"], continue_b)

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

my1 = Button(1450, 65, 400, 100, BUTTONS_PASSIVE[str(ind2)], BUTTONS_ACTIVE[str(ind2)], BUTTONS_ACTIVE[str(ind2)],
             lambda x=CHARACTERS[ind2]: you.add(x))
my2 = Button(1450, 215, 400, 100, BUTTONS_PASSIVE[str(ind2 + 1)], BUTTONS_ACTIVE[str(ind2 + 1)],
             BUTTONS_ACTIVE[str(ind2 + 1)], lambda x=CHARACTERS[ind2 + 1]: you.add(x))
my3 = Button(1450, 365, 400, 100, BUTTONS_PASSIVE[str(ind2 + 2)], BUTTONS_ACTIVE[str(ind2 + 2)],
             BUTTONS_ACTIVE[str(ind2 + 2)], lambda x=CHARACTERS[ind2 + 2]: you.add(x))
my4 = Button(1450, 515, 400, 100, BUTTONS_PASSIVE[str(ind2 + 3)], BUTTONS_ACTIVE[str(ind2 + 3)],
             BUTTONS_ACTIVE[str(ind2 + 3)], lambda x=CHARACTERS[ind2 + 3]: you.add(x))
my5 = Button(1450, 665, 400, 100, BUTTONS_PASSIVE[str(ind2 + 4)], BUTTONS_ACTIVE[str(ind2 + 4)],
             BUTTONS_ACTIVE[str(ind2 + 4)], lambda x=CHARACTERS[ind2 + 4]: you.add(x))


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
            ideal2 = Button(x1, y1 + 150, 400, 100, BUTTONS_PASSIVE[str(ind + 1)], BUTTONS_ACTIVE[str(ind + 1)],
                            BUTTONS_ACTIVE[str(ind + 1)], lambda x=CHARACTERS[ind + 1]: ideal.add(x))
            ideal3 = Button(x1, y1 + 300, 400, 100, BUTTONS_PASSIVE[str(ind + 2)], BUTTONS_ACTIVE[str(ind + 2)],
                            BUTTONS_ACTIVE[str(ind + 2)], lambda x=CHARACTERS[ind + 2]: ideal.add(x))
            ideal4 = Button(x1, y1 + 450, 400, 100, BUTTONS_PASSIVE[str(ind + 3)], BUTTONS_ACTIVE[str(ind + 3)],
                            BUTTONS_ACTIVE[str(ind + 3)], lambda x=CHARACTERS[ind + 3]: ideal.add(x))
            ideal5 = Button(x1, y1 + 600, 400, 100, BUTTONS_PASSIVE[str(ind + 4)], BUTTONS_ACTIVE[str(ind + 4)],
                            BUTTONS_ACTIVE[str(ind + 4)], lambda x=CHARACTERS[ind + 4]: ideal.add(x))


class Scroll2:
    def __init__(self, x1, y1, x2, y2):
        global ind2
        global my1, my2, my3, my4, my5
        mouse = pygame.mouse.get_pos()
        if x1 < mouse[0] < x2 and y1 < mouse[1] < y2:
            if event.button == 4:
                ind2 -= 1
                if ind2 < 0:
                    ind2 = 0
            elif event.button == 5:
                ind2 += 1
                if ind2 > len(CHARACTERS) - 5:
                    ind2 = len(CHARACTERS) - 5

            my1.kill()
            my2.kill()
            my3.kill()
            my4.kill()
            my5.kill()

            my1 = Button(x1, y1, 400, 100, BUTTONS_PASSIVE[str(ind2)], BUTTONS_ACTIVE[str(ind2)],
                         BUTTONS_ACTIVE[str(ind2)],
                         lambda x=CHARACTERS[ind2]: ideal.add(x))
            my2 = Button(x1, y1 + 150, 400, 100, BUTTONS_PASSIVE[str(ind2 + 1)], BUTTONS_ACTIVE[str(ind2 + 1)],
                         BUTTONS_ACTIVE[str(ind2 + 1)], lambda x=CHARACTERS[ind2 + 1]: ideal.add(x))
            my3 = Button(x1, y1 + 300, 400, 100, BUTTONS_PASSIVE[str(ind2 + 2)], BUTTONS_ACTIVE[str(ind2 + 2)],
                         BUTTONS_ACTIVE[str(ind2 + 2)], lambda x=CHARACTERS[ind2 + 2]: ideal.add(x))
            my4 = Button(x1, y1 + 450, 400, 100, BUTTONS_PASSIVE[str(ind2 + 3)], BUTTONS_ACTIVE[str(ind2 + 3)],
                         BUTTONS_ACTIVE[str(ind2 + 3)], lambda x=CHARACTERS[ind2 + 3]: ideal.add(x))
            my5 = Button(x1, y1 + 600, 400, 100, BUTTONS_PASSIVE[str(ind2 + 4)], BUTTONS_ACTIVE[str(ind2 + 4)],
                         BUTTONS_ACTIVE[str(ind2 + 4)], lambda x=CHARACTERS[ind2 + 4]: ideal.add(x))


cursor = Cursor()

clock = pygame.time.Clock()
FPS = 60
running = True
pygame.mouse.set_visible(False)

while running:
    font = pygame.font.Font("data/fonts/RammettoOne-Regular.ttf", 90)
    text = font.render(prom_age, True, (0, 0, 0))
    for event in pygame.event.get():
        Spinbox(810, 700, 1110, 850)
        if event.type == pygame.MOUSEBUTTONDOWN:
            Scroll1(70, 65, 470, 765)
            Scroll2(1450, 65, 1850, 765)
        elif event.type == pygame.KEYDOWN:
            pass
        button_group.update(event)

    screen.fill(pygame.Color("#DF1479"))
    draw_image("woman.png", 873, 188)
    draw_image("pole.png", 810, 700)
    screen.blit(text, (880, 700))

    render_description(screen, " ".join(ideal), 70, 800)
    render_description(screen, " ".join(you), 1450, 800)

    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(FPS)
    pygame.display.flip()
