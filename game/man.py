from system.constants import HAIRS, FACES, BODIES, PANTS, NAMES, FONTS, CHARACTERS, PROPERTIES, JOBS, CHARACTERS_DICT
from random import random, choice, randint, sample
from configparser import ConfigParser
from system.music import IVAN_SOUND, KONCH_SOUND
import pygame


# Спрайт волос)))
class Hair(pygame.sprite.Sprite):
    def __init__(self, groups, pos_x=889, pos_y=70):
        super().__init__(*groups)

        self.image = choice(HAIRS)[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.groups = groups

    def update(self):
        self.image = choice(HAIRS)[0]


# Спрайт лица с руками)))
class Face(pygame.sprite.Sprite):
    def __init__(self, groups, pos_x=837, pos_y=98):
        super().__init__(*groups)

        self.image = choice(FACES)[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.groups = groups

    def update(self):
        self.image = choice(FACES)[0]


# Спрайт ркбахи)))
class Body(pygame.sprite.Sprite):
    def __init__(self, groups, pos_x=837, pos_y=253):
        super().__init__(*groups)

        self.image = choice(BODIES)[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.groups = groups

    def update(self):
        self.image = choice(BODIES)[0]


# Спрайт ркбахи)))
class Pants(pygame.sprite.Sprite):
    def __init__(self, groups, pos_x=889, pos_y=596):
        super().__init__(*groups)

        self.image = choice(PANTS)[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.groups = groups

    def update(self):
        self.image = choice(PANTS)[0]


# Класс мужичка
class Man:
    # Тупа генератор
    def __init__(self, body, face, pants, hair, player, man_group):
        self.body, self.face, self.pants, self.hair = body, face, pants, hair
        self.player, self.man_group = player, man_group
        self.reject_count = 0
        self.update_man()  # создание мужика
        self.load_from_save()  # загрузка мужика из сохранения

    # Функция создания обновления мужика
    def update_man(self):
        self.man_group.update()  # смена картинок на рандомные у мужика
        self.age = randint(16, 60)  # рандомный возраст
        self.name = choice(NAMES)  # рандомное имя
        self.gender = 'M'  # пол мужичка

        self.wealth_value = 0

        self.job = choice(list(JOBS.keys()))
        self.wealth_value += round(JOBS[self.job] * 2.5)

        self.property = choice(list(PROPERTIES.keys()))
        self.wealth_value += round(PROPERTIES[self.property] * 2.5)

        self.character_value, self.characters = self.create_characters()
        self.compatibility_value = self.create_compatibility(self.player)
        self.happiness_value = (self.compatibility_value + self.character_value + self.wealth_value) // 3
        self.cost = round((self.compatibility_value + self.happiness_value + self.character_value + self.wealth_value) / 4) * 10

        # Обновление характеристик и описания
        self.update_specifications()
        self.update_description()

        # Посхалочки))))
        if round(random(), 9) == 0.000_000_001:
            self.specifications = dict((key, 10) for key in self.specifications.keys())
            IVAN_SOUND.play()
            self.description = 'Иван, 16 лет, реальный пацан, разбирается в мемах и хайповой моде. ' \
                               'Ищет горячую чику постарше.'
        elif round(random(), 9) == 0.000_000_001:
            self.specifications = dict((key, -10) for key in self.specifications.keys())
            KONCH_SOUND.play()
            self.description = 'Ну что тут скажешь, конч за 500.'

    def choice_age_years(self, age):
        if len(str(age)) >= 2:
            if str(age)[-2:] in ('11', '12', '13', '14'):
                return 'лет'
            if str(age)[-1] in ('2', '3', '4'):
                return 'года'
            if str(age)[-1] == '1':
                return 'год'
            return 'лет'
        else:
            if str(age)[-1] in ('2', '3', '4'):
                return 'года'
            if str(age)[-1] == '1':
                return 'год'
            return 'лет'

    def update_description(self):
        self.description = f'{self.name}, {self.age} {self.choice_age_years(self.age)}, работет {self.job}, ' \
                           f'имеет {self.property}, характером он {", ".join(self.characters)}.'

    def update_specifications(self):
        self.specifications = {'Счастье': int(self.happiness_value), 'Достаток': int(self.wealth_value),
                               'Совместимость': int(self.compatibility_value), 'Характер': int(self.character_value)}

    # Функция загрузки мужичка из сохранения
    def load_from_save(self):
        config = ConfigParser()
        config.read('./data/save.ini', encoding='utf8')
        section = 'section_man'
        keys = ['gender', 'age', 'name', 'characters', 'job', 'property', 'happiness_value', 'wealth_value',
                'compatibility_value', 'character_value', 'body', 'face', 'hair', 'pants']
        for key in keys:  # хайповоя замена старых значений
            getattr(self, f'set_{key}')(config.get(section, key))

        # Обновление характеристик и описания
        self.update_specifications()
        self.update_description()

    # Функция для принятия мужичка
    def accept_man(self):
        self.reject_count = 0
        if self.player.money >= 10:
            self.player.money -= 10
            self.player.accept(self.specifications)
            self.update_man()

    # Функция для отказа мужичку
    def reject_man(self):
        self.reject_count += 1
        self.player.money += 3
        if self.reject_count > 2:
            self.player.specifications = {key: value - 15 for key, value in self.player.specifications.items()}
        self.update_man()

    # Функция для вывода описания и характеристик
    def render(self, screen):
        self.render_specifications(screen)
        self.render_description(screen)

    # Функция для вывода характеристик
    def render_specifications(self, screen):
        text = [f'{item[0]}: {item[1]}' for item in self.specifications.items()]
        text = [item[0] for item in self.specifications.items()]
        font = FONTS['Pacifico-Regular-60']
        text_coord = 70
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            intro_rect.x = 1258
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

            radius = 10 if abs(self.specifications[line]) <= 4 else 15
            center_x = 10 + intro_rect.x + intro_rect.width + radius
            center_y = intro_rect.y + intro_rect.height // 2 + radius // 2
            pygame.draw.circle(screen, 'black', (center_x, center_y), radius)

    # Функция для вывода описания
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
        text_coord = 640
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = 1350
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    # Не моя компитенция)))
    def create_compatibility(self, player):
        if player.gender_partner != self.gender:
            return -10

        compatibility_value = 0
        a = [i == j for j in self.characters for i in player.characters_partner]
        b = [CHARACTERS_DICT[i] == j for j in self.characters for i in player.characters_partner]
        compatibility_value += a.count(True) * 3
        compatibility_value += b.count(True) * -3

        age_difference = player.age - self.age
        if age_difference // 10 != 0:
            compatibility_value -= age_difference // 10
        else:
            compatibility_value += age_difference % 10
        return compatibility_value

    def create_characters(self):
        characters = sample(CHARACTERS, randint(3, 7))
        character_value = 0
        for i, character in enumerate(characters):
            ind = randint(0, 1)
            character_value += 1 * 2 * (ind if ind != 0 else -1)
            characters[i] = character[ind]
        return character_value, characters

    # Функция сохранения мужичка
    def save_progress(self):
        config = ConfigParser()
        config.read('./data/save.ini', encoding='utf8')
        section = 'section_man'
        # хайповй список характеристик мужичка
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

        with open('./data/save.ini', 'w', encoding='utf8') as configfile:
            config.write(configfile)

    # Куча методов для изменения характеристик мужичка
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
