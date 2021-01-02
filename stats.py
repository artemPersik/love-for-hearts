import random
import pymorphy2
import math

morph = pymorphy2.MorphAnalyzer()
# это характеристики игрока потом при старте игры надо будет их делать
player = {"gender": "W",
          "gender_partner": "M",
          "age": 20,
          "character": ['ЗОЖник', 'щедрый', 'добрый'],
          "character_partner": ['ЗОЖник', 'щедрый', 'добрый']}

my_age = player["age"]
# тут статы из которых генерируетс всё
names = ["Иван", "Артём", "Влад", "Женя", "Никита", "Виталик", "Петя", "Жора", "Гена", "Роберт", "Тимур", "Саша",
         "Миша", "Лёша", "Алан", "Вова", "Богдан", "Армэн",
         "Карэн", "Альберт", "Дима", "Лев", "Стас", "Самуэль", "Джон", "Павел", "Сава", "Стёпа", "Рэн", "Рустам",
         "Олег", "Ян", "Иосиф", "Денис", "Слава", "Артур", "Рик"]

characters = {
    "negative": ['алкаголик', 'жадина', 'злобный', 'раздрожительный', 'высокаомерный', 'лицимер', 'эгоистичен',
                 'жесток', "ленивый"],
    "passive": ['жизнерадостный', 'реалист'],
    "positive": ['ЗОЖник', 'щедрый', 'добрый', 'спокойный', 'скромный', 'прямолинейный', 'заботливый', 'добрый',
                 "активный"]}

jobs = {"beggar": ['никем', 'дворником', 'в макдональдсе', 'уборщиком', 'грузсчиком'],
        "medium": ['строителем', 'врачом', 'мелкийм предпинемателем', 'инженером', 'сантехником', 'эллектриком',
                   'пилотом'],
        "high": ['бизнессмеом', 'нефтяником', 'банкиром', 'айтишником']}

property = {"low": ['ночего'],
            "medium": ['квартиру', 'машину'],
            "high": ["квартиру и машину"]}
# генерация имени и возроста
name = names[random.randint(0, len(names) - 1)]
age = random.randint(18, my_age + 20)


def character():  # функция характера

    character_negative = []
    character_passive = []
    character_possitive = []

    for _ in range(random.randint(1, 7)):
        character_negative.append(characters["negative"][random.randint(0, len(characters["negative"]) - 1)])
    for _ in range(random.randint(1, 13)):
        ind = random.randint(1, len(characters["negative"]) - 1)
        for i in character_negative:
            if ind == characters["negative"].index(i):
                pass
            else:
                character_possitive.append(characters["positive"][ind])
    for _ in range(random.randint(1, 7)):
        character_passive.append(characters["passive"][random.randint(0, len(characters["passive"]) - 1)])
    character_des = character_possitive + character_passive + character_negative
    character = len(set(character_negative)) * -2 + len(set(character_passive)) * 1 + len(set(character_possitive)) * 2
    if character > 10:
        character = 10
    elif character < -10:
        character = -10
    return set(character_des), character


def wealth(): # функция достатка
    wealth_prom = 0
    property_prom = ""
    job_prom = ""
    procent = random.randint(0, 101)
    procent2 = random.randint(0, 101)
    if procent <= 20:
        wealth_prom -= 5
        property_prom = (property["low"][random.randint(0, len(property["low"])) - 1])
    elif procent > 20 and procent <= 90:
        wealth_prom += 3
        property_prom = (property["medium"][random.randint(0, len(property["medium"])) - 1])
    elif procent > 90:
        wealth_prom += 5
        property_prom = (property["high"][random.randint(0, len(property["high"])) - 1])

    if procent2 <= 20:
        wealth_prom -= 5
        job_prom = (jobs["beggar"][random.randint(0, len(jobs["beggar"])) - 1])
    elif procent2 > 20 and procent <= 90:
        wealth_prom += 3
        job_prom = (jobs["medium"][random.randint(0, len(jobs["medium"])) - 1])
    elif procent2 > 90:
        wealth_prom += 5
        job_prom = (jobs["high"][random.randint(0, len(jobs["high"])) - 1])

    return wealth_prom, job_prom, property_prom


def compatibility(player, gender, character_p): # функция совместимости, словарь игрока пол партнёра, характер партнёра
    compatibility_prom = 0
    if gender != player["gender_partner"]:
        return -10

    for i in player["character_partner"]:
        if i in character_p:
            compatibility_prom += 2

    for i in player["character"]:
        if i in characters["positive"]:
            ind = characters["positive"].index(i)
            for j in character_p:
                if j in characters["negative"]:
                    if characters["negative"].index(j) == ind:
                        compatibility_prom -= 1

    for i in player["character"]:
        if i in characters["negative"]:
            ind = characters["negative"].index(i)
            for j in character_p:
                if j in characters["positive"]:
                    if characters["positive"].index(j) == ind:
                        compatibility_prom -= 1

    if age - my_age >= math.fabs(5):
        compatibility_prom += 2
    else:
        compatibility_prom -= 2

    compatibility_prom + random.randint(-3, 3)

    if compatibility_prom < -10:
        return -10
    elif compatibility_prom > 10:
        return 10
    else:
        return compatibility_prom


a = morph.parse('лет')[0]
a_n = a.make_agree_with_number(age).word

# класс партнёра
class Partner:
    def __init__(self, player, gender):
        self.character_full = character()
        self.wealth_full = wealth()

        self.wealth = self.wealth_full[0]
        self.character = self.character_full[1]
        self.compatibility = compatibility(player, gender, self.character_full[0])
        self.happiness = int(self.compatibility // 2 + self.wealth // 3 + self.character // 3)
        if self.happiness < -10:
            self.happiness = -10
        elif self.happiness > 10:
            self.happiness = 10

        self.description = f"{name}, {age} {a_n}, работет {self.wealth_full[1]}, " \
                           f"имеет {self.wealth_full[2]}, характером он {', '.join(character()[0])}"

    def __str__(self):
        return self.description

    def ret(self):
        return self.happiness, self.wealth, self.compatibility, self.character


def main(player, gender):
    par = Partner(player, gender)
    procent = random.randint(0, 101)
    if procent <= 98:
        return str(par), par.ret()
    elif procent == 99:
        return "иван 16 лет реальный пацан разбирается в мемах и хайповой моде ищет горячую чику постарше", (10, 10, 10, 10)
    elif procent == 100:
        return "конч за 500, что тут сказать", (-10, -10, -10, -10)

print(main(player, "M"))

