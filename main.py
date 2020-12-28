from random import choice, randint
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


def load_clothes(name):
    fullname = os.path.join(f'data\\lists_clothes', name)
    if not os.path.isfile(fullname):
        print(f"Файл с одеждой '{fullname}' не найден")
        sys.exit()
    with open(fullname, 'r', encoding='utf8') as file:
        lines = map(lambda x: x.rstrip().split(), file.readlines())
    return lines


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


class Hair(pygame.sprite.Sprite):
    def __init__(self, pos_x=889, pos_y=70):
        super().__init__(man_group, all_sprites)

        self.image = choice(HAIRS)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.image = choice(HAIRS)


class Face(pygame.sprite.Sprite):
    def __init__(self, pos_x=837, pos_y=98):
        super().__init__(man_group, all_sprites)

        self.image = choice(FACES)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.image = choice(FACES)


class Body(pygame.sprite.Sprite):
    def __init__(self, pos_x=837, pos_y=253):
        super().__init__(man_group, all_sprites)

        self.image = choice(BODIES)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.image = choice(BODIES)


class Pants(pygame.sprite.Sprite):
    def __init__(self, pos_x=889, pos_y=596):
        super().__init__(man_group, all_sprites)

        self.image = choice(PANTS)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.image = choice(PANTS)


class Man:
    def __init__(self, body, face, pants, hair):
        self.body, self.face, self.pants, self.hair = body, face, pants, hair
        self.specifications = {'Стата1': randint(-10, 10), 'Сатата2': randint(-10, 10),
                               'Стата3': randint(-10, 10), 'Сатата4': randint(-10, 10)}

    def update_man(self):
        man_group.update()
        self.specifications = {'Стата1': randint(-10, 10), 'Сатата2': randint(-10, 10),
                               'Стата3': randint(-10, 10), 'Сатата4': randint(-10, 10)}

    def accept_man(self):
        player.accept(self.specifications)
        self.update_man()

    def reject_man(self):
        self.update_man()

    def render(self, screen):
        text = [f'{item[0]}: {item[1]}' for item in self.specifications.items()]
        font = pygame.font.Font(None, 70)
        text_coord = 107
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 124
            intro_rect.top = text_coord
            intro_rect.x = 1258
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)


class Player:
    def __init__(self, num1=5, num2=5, num3=5, num4=5):
        self.specifications = {'Стата1': num1, 'Сатата2': num2, 'Стата3': num3, 'Сатата4': num4}

    def accept(self, man_specifications):
        self.specifications = dict((key, self.specifications[key] + man_specifications[key])
                                   for key in man_specifications.keys())

    def render(self, screen):
        text = [f'{item[0]}: {item[1]}' for item in self.specifications.items()]
        font = pygame.font.Font(None, 70)
        text_coord = 107
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 124
            intro_rect.top = text_coord
            intro_rect.x = 70
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)


pygame.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
man_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()

FACES = list(map(lambda x: load_image(x[1], x[0]), load_clothes('faces.txt')))
HAIRS = list(map(lambda x: load_image(x[1], x[0]), load_clothes('hairs.txt')))
BODIES = list(map(lambda x: load_image(x[1], x[0]), load_clothes('T-shirts.txt')))
PANTS = list(map(lambda x: load_image(x[1], x[0]), load_clothes('pants.txt')))
cursor_image = load_image('cursor.png')
empty_image = load_image('empty.png')

man = Man(Body(), Face(), Pants(), Hair())
player = Player()

reject_button = Button(611, 950, 300, 75, 'menu_button1.png', 'menu_button2.png', 'menu_button2.png', man.reject_man)
accept_button = Button(1023, 950, 300, 75, 'menu_button1.png', 'menu_button2.png', 'menu_button2.png', man.accept_man)
cursor = Cursor()

clock = pygame.time.Clock()
FPS = 50
running = True
pygame.mouse.set_visible(False)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button_group.update(event)

    screen.fill('#DF1479')

    man.render(screen)
    player.render(screen)
    all_sprites.draw(screen)

    cursor.update()
    pygame.display.flip()

pygame.quit()
