from constants import HAIRS, FACES, BODIES, PANTS, NAMES, FONTS, CHARACTERS, PROPERTIES, JOBS
from random import random, choice, randint
from configparser import ConfigParser
from music import IVAN_SOUND, KONCH_SOUND
from math import fabs
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
        self.update_man()  # создание мужика
        self.load_from_save()  # загрузка мужика из сохранения

    # Функция создания/обновления мужика
    def update_man(self):
        self.man_group.update()  # смена картинок на рандомные у мужика
        self.age = randint(16, 60)  # рандомный возраст
        self.name = choice(NAMES)  # рандомное имя
        self.gender = 'M'  # пол мужичка

        # Хз, что за дичь писал не я)))
        self.character_full = self.create_character()
        self.wealth_full = self.create_wealth()
        self.wealth = self.wealth_full[0]
        self.character = self.character_full[1]
        self.compatibility = self.create_compatibility(self.player, self.gender, self.character_full[0])
        self.happines = self.create_happiness()

        self.job = self.wealth_full[1]
        self.property = self.wealth_full[2]
        self.characters = self.character_full[0]

        # Обновление характеристик и описания
        self.update_specifications()
        self.update_description()

        # Посхалочки))))
        if round(random(), 6) == 0.000001:
            self.specifications = dict((key, 10) for key in self.specifications.keys())
            IVAN_SOUND.play()
            self.description = 'Иван, 16 лет, реальный пацан, разбирается в мемах и хайповой моде. ' \
                               'Ищет горячую чику постарше.'
        elif round(random(), 6) == 0.000001:
            self.specifications = dict((key, -10) for key in self.specifications.keys())
            KONCH_SOUND.play()
            self.description = 'Ну что тут скажешь, конч за 500.'

    def update_description(self):
        self.description = f'{self.name}, {self.age} годов, работет {self.job}, ' \
                           f'имеет {self.property}, характером он {", ".join(self.characters)}'

    def update_specifications(self):
        self.specifications = {'Счастье': int(self.happines), 'Достаток': int(self.wealth),
                               'Совместимость': int(self.compatibility), 'Характер': int(self.character)}

    # Функция загрузки мужичка из сохранения
    def load_from_save(self):
        config = ConfigParser()
        config.read('save.ini', encoding='utf8')
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
        self.player.accept(self.specifications)
        self.update_man()

    # Функция для отказа мужичку
    def reject_man(self):
        self.update_man()

    # Функция для вывода описания и характеристик
    def render(self, screen):
        self.render_specifications(screen)
        self.render_description(screen)

    # Функция для вывода характеристик
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
        text_coord = 600
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = 1350
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    # Не моя компитенция)))
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

        if self.age - player.age >= fabs(5):
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

    # Не моя компитенция)))
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

    # Не моя компитенция)))
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

    # Не моя компитенция)))
    def create_happiness(self):
        happiness = int(self.compatibility // 2 + self.wealth // 3 + self.character // 3)
        if happiness < -10:
            happiness = -10
        elif happiness > 10:
            happiness = 10
        return happiness

    # Функция сохранения мужичка
    def save_progress(self):
        config = ConfigParser()
        config.read('save.ini', encoding='utf8')
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

        with open('save.ini', 'w', encoding='utf8') as configfile:
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
