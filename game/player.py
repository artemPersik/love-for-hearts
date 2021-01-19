from configparser import ConfigParser
from system.constants import FONTS


# Класс игрока
class Player:
    def __init__(self):
        self.specifications = {}
        self.load_from_save()

    def accept(self, man_specifications):
        self.specifications = dict((key, self.specifications[key] + man_specifications[key])
                                   for key in man_specifications.keys())

    def render(self, screen):
        text = [f'{item[0]}: {item[1]}' for item in self.specifications.items()]
        font = FONTS['Pacifico-Regular-60']
        text_coord = 70
        for line in text:
            string_rendered = font.render(line, 1, 'black')
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            intro_rect.x = 110
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def save_progress(self):
        config = ConfigParser()
        config.read('./data/save.ini', encoding='utf8')
        section = 'section_player'
        values = [('gender', self.gender), ('gender_partner', self.gender_partner), ('age', str(self.age)),
                  ('characters', ' '.join(self.characters)), ('characters_partner', ' '.join(self.characters_partner)),
                  ('happiness_value', str(self.specifications['Счастье'])),
                  ('wealth_value', str(self.specifications['Достаток'])),
                  ('compatibility_value', str(self.specifications['Совместимость'])),
                  ('character_value', str(self.specifications['Характер'])),
                  ('money', str(self.money))]

        for value1, value2 in values:
            config.set(section, value1, value2)

        with open('./data/save.ini', 'w', encoding='utf8') as configfile:
            config.write(configfile)

    def load_from_save(self):
        config = ConfigParser()
        config.read('./data/save.ini', encoding='utf8')
        section = 'section_player'
        keys = ['gender', 'gender_partner', 'age', 'characters', 'characters_partner', 'happiness_value',
                'wealth_value', 'compatibility_value', 'character_value', 'money']

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

    def set_gender_partner(self, gender):
        if gender != 'null':
            self.gender_partner = gender
        else:
            self.gender_partner = 'M'

    def set_characters(self, characters):
        if characters != 'null':
            self.characters = characters.split()

    def set_characters_partner(self, characters):
        if characters != 'null':
            self.characters_partner = characters.split()

    def set_happiness_value(self, value):
        if value != 'null':
            self.specifications['Счастье'] = int(value)
        else:
            self.specifications['Счастье'] = 25

    def set_wealth_value(self, value):
        if value != 'null':
            self.specifications['Достаток'] = int(value)
        else:
            self.specifications['Достаток'] = 25

    def set_compatibility_value(self, value):
        if value != 'null':
            self.specifications['Совместимость'] = int(value)
        else:
            self.specifications['Совместимость'] = 25

    def set_character_value(self, value):
        if value != 'null':
            self.specifications['Характер'] = int(value)
        else:
            self.specifications['Характер'] = 25

    def set_money(self, value):
        if value != 'null':
            self.money = int(value)
        else:
            self.money = 150
