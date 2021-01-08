from random import choice, randint, random
from configparser import ConfigParser
import pygame
import math
import sys
import os
from music import music


def save_game_progress(player, man):
    player.save_progress()
    man.save_progress()


def get_volume_from_save():
    config = ConfigParser()
    config.read('save.ini', encoding='utf8')
    section = 'section_settings'
    return config.getfloat(section, 'volume')


def save_settings(**settings):
    config = ConfigParser()
    config.read('save.ini', encoding='utf8')
    section = 'section_settings'
    for setting, value in settings.items():
        config.set(section, setting, str(value))

    with open('save.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)


def terminate():
    pygame.quit()
    sys.exit()


def restart_game():
    config = ConfigParser()
    config.read('save.ini', encoding='utf8')
    section = 'section_man'
    keys = ['gender', 'age', 'name', 'characters', 'job', 'property', 'happiness_value', 'wealth_value',
            'compatibility_value', 'character_value', 'body', 'face', 'hair', 'pants']

    for key in keys:
        config.set(section, key, 'null')

    section = 'section_player'
    keys = ['gender', 'gender_partner', 'age', 'characters', 'characters_partner', 'happiness_value',
            'wealth_value', 'compatibility_value', 'character_value']

    for key in keys:
        config.set(section, key, 'null')

    with open('save.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)


def load_image(name, path='', colorkey=None):
    fullname = os.path.join(f'data/images{path}', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_clothes(name):
    fullname = os.path.join(f'data/lists_clothes', name)
    if not os.path.isfile(fullname):
        print(f"Файл с одеждой '{fullname}' не найден")
        sys.exit()
    with open(fullname, 'r', encoding='utf8') as file:
        path = file.readline().rstrip()
        lines = map(lambda x: (path, x.rstrip()), file.readlines())
    return list(lines).copy()


def main_game():
    music.music_sausage()
    player = Player()
    man = Man(Body(), Face(), Pants(), Hair(), player)

    Button(611, 950, 300, 75, IMAGES['reject1'], IMAGES['reject2'], IMAGES['reject2'], man.reject_man)
    Button(1023, 950, 300, 75, IMAGES['accept1'], IMAGES['accept2'], IMAGES['accept2'], man.accept_man)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                save_game_progress(player, man)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_game_progress(player, man)
                all_sprites.empty()
                button_group.empty()
                man_group.empty()
                return
            button_group.update(event)

        screen.fill('#DF1479')

        man.render(screen)
        player.render(screen)
        all_sprites.draw(screen)

        cursor.update()
        pygame.display.flip()


def pause_menu():
    continue_btn = Button(660, 100, 600, 150, IMAGES['continue1'], IMAGES['continue2'], IMAGES['continue2'], None)
    restart_btn = Button(660, 300, 600, 150, IMAGES['restart1'], IMAGES['restart2'], IMAGES['restart2'], None)
    quit_btn = Button(660, 700, 600, 150, IMAGES['quit1'], IMAGES['quit2'], IMAGES['quit2'], terminate)
    volume_slider = VolumeSlider((660, 500), IMAGES['line_slider'], (600, 100), (600, 150),
                                 Slider(IMAGES['slider']), get_volume_from_save())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or continue_btn.is_mouse_button_up(event):
                all_sprites.empty()
                button_group.empty()
                save_settings(volume=volume_slider.get_volume())
                return

            if restart_btn.is_mouse_button_up(event):
                all_sprites.empty()
                button_group.empty()
                save_settings(volume=volume_slider.get_volume())
                restart_game()
                return
            button_group.update(event)
            volume_slider.update(event)

        screen.fill('#DF1479')
        all_sprites.draw(screen)

        cursor.update()
        pygame.display.flip()


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = CURSOR_IMAGE
        self.rect = self.image.get_rect()

    def update(self):
        if pygame.mouse.get_focused():
            self.rect.x, self.rect.y = pygame.mouse.get_pos()

        if self not in all_sprites:
            all_sprites.add(self)


class AllSprites(pygame.sprite.Group):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        sprites.sort(key=lambda x: isinstance(x, Slider))
        sprites.sort(key=lambda x: isinstance(x, Cursor))
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


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
            if self.func is not None:
                music.btn_sound.play()
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
        self.pass_image = image

    def set_direct_image(self, image):
        self.direct_image = image

    def set_clicked_image(self, image):
        self.clicked_image = image

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


class Slider(pygame.sprite.Sprite):
    def __init__(self, image, size=None):
        super().__init__(all_sprites)
        if size is not None:
            image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect()

    def move_to(self, pos_x, pos_y):
        self.rect.x, self.rect.y = pos_x, pos_y


class VolumeSlider(pygame.sprite.Sprite):
    def __init__(self, pos, line_image, line_size, size, slider, volume):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(line_image, line_size)
        self.rect = self.image.get_rect().move(pos[0], pos[1] + (size[1] - line_size[1]) // 2)
        self.volume_slider = pygame.Rect(*pos, *size)
        self.slider, self.volume, self.flag = slider, volume, False
        self.slider.rect.x, self.slider.rect.y = size[0] * volume + pos[0] - slider.rect.width // 2, pos[1]

        self.pos_x, self.pos_y = pos
        self.width, self.height = size
        self.slider_width, self.slider_height = self.rect.size

    def fix_slider_coord(self):
        if self.slider.rect.x < self.rect.x - self.slider.rect.width // 2:
            self.slider.rect.x = self.rect.x - self.slider.rect.width // 2
        elif self.slider.rect.x > self.rect.x + self.rect.width - self.slider.rect.width // 2:
            self.slider.rect.x = self.rect.x + self.rect.width - self.slider.rect.width // 2

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.volume_slider.collidepoint(event.pos):
            self.slider.rect.x = event.pos[0]
            self.flag = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.flag = False

        if event.type == pygame.MOUSEMOTION and self.flag:
            self.slider.rect.x += event.rel[0]
            self.fix_slider_coord()

        if event.type == pygame.MOUSEWHEEL:
            self.slider.rect.x += event.y * self.slider.rect.width // 20
            self.fix_slider_coord()
        self.volume = round((self.slider.rect.x - self.rect.x + self.slider.rect.width // 2) / self.rect.width, 2)

    def get_volume(self):
        return self.volume


class Hair(pygame.sprite.Sprite):
    def __init__(self, pos_x=889, pos_y=70):
        super().__init__(man_group, all_sprites)

        self.image = choice(HAIRS)[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.image = choice(HAIRS)[0]


class Face(pygame.sprite.Sprite):
    def __init__(self, pos_x=837, pos_y=98):
        super().__init__(man_group, all_sprites)

        self.image = choice(FACES)[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.image = choice(FACES)[0]


class Body(pygame.sprite.Sprite):
    def __init__(self, pos_x=837, pos_y=253):
        super().__init__(man_group, all_sprites)

        self.image = choice(BODIES)[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.image = choice(BODIES)[0]


class Pants(pygame.sprite.Sprite):
    def __init__(self, pos_x=889, pos_y=596):
        super().__init__(man_group, all_sprites)

        self.image = choice(PANTS)[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.image = choice(PANTS)[0]


class Man:
    def __init__(self, body, face, pants, hair, player):
        self.body, self.face, self.pants, self.hair = body, face, pants, hair
        self.player = player
        self.update_man()
        self.load_from_save()

    def update_man(self):
        man_group.update()
        self.age = randint(16, 60)
        self.name = choice(NAMES)
        self.gender = 'M'

        self.character_full = self.create_character()
        self.wealth_full = self.create_wealth()
        self.wealth = self.wealth_full[0]
        self.character = self.character_full[1]
        self.compatibility = self.create_compatibility(self.player, self.gender, self.character_full[0])
        self.happines = self.create_happiness()

        self.job = self.wealth_full[1]
        self.property = self.wealth_full[2]
        self.characters = self.character_full[0]

        self.update_specifications()
        self.update_description()

        if round(random(), 2) == 0.01:
            self.specifications = dict((key, 10) for key in self.specifications.keys())
            self.description = 'Иван, 16 лет, реальный пацан, разбирается в мемах и хайповой моде. ' \
                               'Ищет горячую чику постарше.'
            music.ivan_sound.play()
        elif round(random(), 2) == 0.01:
            self.specifications = dict((key, -10) for key in self.specifications.keys())
            self.description = 'Ну что тут скажешь, конч за 500.'

    def update_description(self):
        self.description = f'{self.name}, {self.age} годов, работет {self.job}, ' \
                           f'имеет {self.property}, характером он {", ".join(self.characters)}'

    def update_specifications(self):
        self.specifications = {'Счастье': int(self.happines), 'Достаток': int(self.wealth),
                               'Совместимость': int(self.compatibility), 'Характер': int(self.character)}

    def load_from_save(self):
        config = ConfigParser()
        config.read('save.ini', encoding='utf8')
        section = 'section_man'
        keys = ['gender', 'age', 'name', 'characters', 'job', 'property', 'happiness_value', 'wealth_value',
                'compatibility_value', 'character_value', 'body', 'face', 'hair', 'pants']
        for key in keys:
            getattr(self, f'set_{key}')(config.get(section, key))
        self.update_specifications()
        self.update_description()

    def accept_man(self):
        self.player.accept(self.specifications)
        self.update_man()

    def reject_man(self):
        self.update_man()

    def render(self, screen):
        self.render_specifications(screen)
        self.render_description(screen)

    def render_specifications(self, screen):
        text = [f'{item[0]}: {item[1]}' for item in self.specifications.items()]
        font = FONTS['Pacifico-Regular-60']
        text_coord = 10
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            intro_rect.x = 1258
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def render_description(self, screen):
        text = []
        line = ''

        for i, word in enumerate(self.description.split()):
            if len(line) + len(word) <= 37:
                line += f' {word}'
            else:
                text.append(line[1:])
                line = f' {word}'

            if i == len(self.description.split()) - 1:
                text.append(line[1:])

        font = FONTS['Pacifico-Regular-30']
        text_coord = 600
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = 1350
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def create_compatibility(self, player, gender, character_p):
        compatibility_prom = 0
        if gender != player.gender_partner:
            return -10

        for i in player.characters_partner:
            if i in character_p:
                compatibility_prom += 2

        for i in player.characters:
            if i in CHARACTERS["positive"]:
                ind = CHARACTERS["positive"].index(i)
                for j in character_p:
                    if j in CHARACTERS["negative"]:
                        if CHARACTERS["negative"].index(j) == ind:
                            compatibility_prom -= 1

        for i in player.characters:
            if i in CHARACTERS["negative"]:
                ind = CHARACTERS["negative"].index(i)
                for j in character_p:
                    if j in CHARACTERS["positive"]:
                        if CHARACTERS["positive"].index(j) == ind:
                            compatibility_prom -= 1

        if self.age - player.age >= math.fabs(5):
            compatibility_prom += 2
        else:
            compatibility_prom -= 2

        compatibility_prom + randint(-3, 3)

        if compatibility_prom < -10:
            return -10
        elif compatibility_prom > 10:
            return 10
        else:
            return compatibility_prom

    def create_character(self):

        character_negative = []
        character_passive = []
        character_positive = []

        for _ in range(randint(1, 7)):
            character_negative.append(choice(CHARACTERS["negative"]))
        for _ in range(randint(1, 13)):
            ind = randint(1, len(CHARACTERS["negative"]) - 1)
            for i in character_negative:
                if ind != CHARACTERS["negative"].index(i):
                    character_positive.append(CHARACTERS["positive"][ind])
        for _ in range(randint(1, 7)):
            character_passive.append(choice(CHARACTERS["passive"]))
        character_des = character_positive + character_passive + character_negative
        character = len(set(character_negative)) * -2 + len(set(character_passive)) * 1 + len(
            set(character_positive)) * 2
        if character > 10:
            character = 10
        elif character < -10:
            character = -10
        return set(character_des), character

    def create_wealth(self):
        wealth_prom = 0
        property_prom = ""
        job_prom = ""
        procent = randint(0, 101)
        procent2 = randint(0, 101)
        if procent <= 20:
            wealth_prom -= 5
            property_prom = (choice(PROPERTIES["low"]))
        elif 20 < procent <= 90:
            wealth_prom += 3
            property_prom = (choice(PROPERTIES["medium"]))
        elif procent > 90:
            wealth_prom += 5
            property_prom = (choice(PROPERTIES["high"]))

        if procent2 <= 20:
            wealth_prom -= 5
            job_prom = (choice(JOBS["beggar"]))
        elif procent2 > 20 and procent <= 90:
            wealth_prom += 3
            job_prom = (choice(JOBS["medium"]))
        elif procent2 > 90:
            wealth_prom += 5
            job_prom = (choice(JOBS["high"]))

        return wealth_prom, job_prom, property_prom

    def create_happiness(self):
        happiness = int(self.compatibility // 2 + self.wealth // 3 + self.character // 3)
        if happiness < -10:
            happiness = -10
        elif happiness > 10:
            happiness = 10
        return happiness

    def save_progress(self):
        config = ConfigParser()
        config.read('save.ini', encoding='utf8')
        section = 'section_man'
        values = [('gender', self.gender), ('age', str(self.age)), ('name', self.name),
                  ('characters', ' '.join(self.characters)), ('job', self.job), ('property', self.property),
                  ('happiness_value', str(self.specifications['Счастье'])),
                  ('wealth_value', str(self.specifications['Достаток'])),
                  ('compatibility_value', str(self.specifications['Совместимость'])),
                  ('character_value', str(self.specifications['Характер'])),
                  ('body', ' '.join(dict(BODIES)[self.body.image])), ('face', ' '.join(dict(FACES)[self.face.image])),
                  ('hair', ' '.join(dict(HAIRS)[self.hair.image])), ('pants', ' '.join(dict(PANTS)[self.pants.image]))]

        for value1, value2 in values:
            config.set(section, value1, value2)

        with open('save.ini', 'w', encoding='utf8') as configfile:
            config.write(configfile)

    def set_body(self, body):
        if body != 'null':
            path, name = body.split()
            self.body.image = dict(item[::-1] for item in BODIES)[path, name]

    def set_face(self, face):
        if face != 'null':
            path, name = face.split()
            self.face.image = dict(item[::-1] for item in FACES)[path, name]

    def set_hair(self, hair):
        if hair != 'null':
            path, name = hair.split()
            self.hair.image = dict(item[::-1] for item in HAIRS)[path, name]

    def set_pants(self, pants):
        if pants != 'null':
            path, name = pants.split()
            self.pants.image = dict(item[::-1] for item in PANTS)[path, name]

    def set_gender(self, gender):
        if gender != 'null':
            self.gender = gender

    def set_age(self, age):
        if age != 'null':
            self.age = int(age)

    def set_name(self, name):
        if name != 'null':
            self.name = name

    def set_job(self, job):
        if job != 'null':
            self.job = job

    def set_characters(self, characters):
        if characters != 'null':
            self.characters = characters.split()

    def set_property(self, pproperty):
        if pproperty != 'null':
            self.property = pproperty

    def set_happiness_value(self, value):
        if value != 'null':
            self.happines = value

    def set_wealth_value(self, value):
        if value != 'null':
            self.wealth = value

    def set_compatibility_value(self, value):
        if value != 'null':
            self.compatibility = value

    def set_character_value(self, value):
        if value != 'null':
            self.character = value


class Player:
    def __init__(self, num1=5, num2=5, num3=5, num4=5):
        self.specifications = {'Счастье': num1, 'Достаток': num2, 'Совместимость': num3, 'Характер': num4}
        self.gender = 'W'
        self.gender_partner = 'M'
        self.age = 20
        self.characters = ['ЗОЖник', 'щедрый', 'добрый']
        self.characters_partner = ['ЗОЖник', 'щедрый', 'добрый']
        self.load_from_save()

    def accept(self, man_specifications):
        self.specifications = dict((key, self.specifications[key] + man_specifications[key])
                                   for key in man_specifications.keys())

    def render(self, screen):
        text = [f'{item[0]}: {item[1]}' for item in self.specifications.items()]
        font = FONTS['Pacifico-Regular-60']
        text_coord = 10
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            intro_rect.x = 70
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def save_progress(self):
        config = ConfigParser()
        config.read('save.ini', encoding='utf8')
        section = 'section_player'
        values = [('gender', self.gender), ('gender_partner', self.gender_partner), ('age', str(self.age)),
                  ('characters', ' '.join(self.characters)), ('characters_partner', ' '.join(self.characters_partner)),
                  ('happiness_value', str(self.specifications['Счастье'])),
                  ('wealth_value', str(self.specifications['Достаток'])),
                  ('compatibility_value', str(self.specifications['Совместимость'])),
                  ('character_value', str(self.specifications['Характер']))]

        for value1, value2 in values:
            config.set(section, value1, value2)

        with open('save.ini', 'w', encoding='utf8') as configfile:
            config.write(configfile)

    def load_from_save(self):
        config = ConfigParser()
        config.read('save.ini', encoding='utf8')
        section = 'section_player'
        keys = ['gender', 'gender_partner', 'age', 'characters', 'characters_partner', 'happiness_value',
                'wealth_value', 'compatibility_value', 'character_value']

        for key in keys:
            getattr(self, f'set_{key}')(config.get(section, key))

    def set_gender(self, gender):
        if gender != 'null':
            self.gender = gender
        else:
            self.gender = 'W'

    def set_age(self, age):
        if age != 'null':
            self.age = int(age)
        else:
            self.age = 20

    def set_gender_partner(self, gender):
        if gender != 'null':
            self.gender_partner = gender
        else:
            self.gender_partner = 'M'

    def set_characters(self, characters):
        if characters != 'null':
            self.characters = characters.split()
        else:
            self.characters = ['ЗОЖник', 'щедрый', 'добрый']

    def set_characters_partner(self, characters):
        if characters != 'null':
            self.characters_partner = characters.split()
        else:
            self.characters_partner = ['ЗОЖник', 'щедрый', 'добрый']

    def set_happiness_value(self, value):
        if value != 'null':
            self.specifications['Счастье'] = int(value)
        else:
            self.specifications['Счастье'] = 5

    def set_wealth_value(self, value):
        if value != 'null':
            self.specifications['Достаток'] = int(value)
        else:
            self.specifications['Достаток'] = 5

    def set_compatibility_value(self, value):
        if value != 'null':
            self.specifications['Совместимость'] = int(value)
        else:
            self.specifications['Совместимость'] = 5

    def set_character_value(self, value):
        if value != 'null':
            self.specifications['Характер'] = int(value)
        else:
            self.specifications['Характер'] = 5


pygame.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(size)
all_sprites = AllSprites()
man_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()

IMAGES = {'continue1': load_image('continue1.png'), 'continue2': load_image('continue2.png'),
          'slider': load_image('slider.png'), 'line_slider': load_image('line_slider.png'),
          'restart1': load_image('restart1.png'), 'restart2': load_image('restart2.png'),
          'accept1': load_image('accept1.png'), 'accept2': load_image('accept2.png'),
          'reject1': load_image('reject1.png'), 'reject2': load_image('reject2.png'),
          'quit1': load_image('quit1.png'), 'quit2': load_image('quit2.png')}
FONTS = {'Pacifico-Regular-60': pygame.font.Font('data/fonts/Pacifico-Regular.ttf', 60),
         'Pacifico-Regular-30': pygame.font.Font('data/fonts/Pacifico-Regular.ttf', 30)}

FACES = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('faces.txt')))
HAIRS = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('hairs.txt')))
BODIES = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('T-shirts.txt')))
PANTS = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('pants.txt')))
CURSOR_IMAGE = load_image('cursor.png')

NAMES = ['Иван', 'Артём', 'Влад', 'Женя', 'Никита', 'Виталик', 'Петя', 'Жора', 'Гена', 'Роберт', 'Тимур', 'Саша',
         'Миша', 'Лёша', 'Алан', 'Вова', 'Богдан', 'Армэн', 'Олег', 'Ян', 'Иосиф', 'Денис', 'Слава', 'Артур', 'Рик',
         'Карэн', 'Альберт', 'Дима', 'Лев', 'Стас', 'Самуэль', 'Джон', 'Павел', 'Сава', 'Стёпа', 'Рэн', 'Рустам']
CHARACTERS = {
    'negative': ['алкаголик', 'жадиный', 'злобный', 'раздрожительный', 'высокомерный', 'лицимер', 'эгоистиченый',
                 'жестокий', "ленивый"],
    'passive': ['жизнерадостный', 'реалист'],
    'positive': ['ЗОЖник', 'щедрый', 'добрый', 'спокойный', 'скромный', 'прямолинейный', 'заботливый', 'активный', 'добрый']}
JOBS = {'beggar': ['никем', 'дворником', 'в макдональдсе', 'уборщиком', 'грузчиком'],
        'medium': ['строителем', 'врачом', 'мелким предпринимателем', 'инженером', 'сантехником', 'электриком',
                   'пилотом'],
        'high': ['бизнессмеом', 'нефтяником', 'банкиром', 'айтишником']}
PROPERTIES = {'low': ['ничего'],
              'medium': ['квартиру', 'машину'],
              'high': ["квартиру и машину"]}

cursor = Cursor()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
FPS = 50

while True:
    main_game()
    pause_menu()