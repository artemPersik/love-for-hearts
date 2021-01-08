from system import load_image, load_clothes
from pygame.font import Font
from pygame import init

init()

IMAGES = {'continue1': load_image('continue1.png'), 'continue2': load_image('continue2.png'),
          'slider': load_image('slider.png'), 'line_slider': load_image('line_slider.png'),
          'restart1': load_image('restart1.png'), 'restart2': load_image('restart2.png'),
          'accept1': load_image('accept1.png'), 'accept2': load_image('accept2.png'),
          'reject1': load_image('reject1.png'), 'reject2': load_image('reject2.png'),
          'quit1': load_image('quit1.png'), 'quit2': load_image('quit2.png')}
FONTS = {'Pacifico-Regular-60': Font('data/fonts/Pacifico-Regular.ttf', 60),
         'Pacifico-Regular-30': Font('data/fonts/Pacifico-Regular.ttf', 30),
         'RammettoOne-Regular-90': Font("data/fonts/RammettoOne-Regular.ttf", 90)}

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
    'positive': ['ЗОЖник', 'щедрый', 'добрый', 'спокойный', 'скромный', 'прямолинейный', 'заботливый', 'активный',
                 'добрый']}
JOBS = {'beggar': ['никем', 'дворником', 'в макдональдсе', 'уборщиком', 'грузчиком'],
        'medium': ['строителем', 'врачом', 'мелким предпринимателем', 'инженером', 'сантехником', 'электриком',
                   'пилотом'],
        'high': ['бизнессмеом', 'нефтяником', 'банкиром', 'айтишником']}
PROPERTIES = {'low': ['ничего'],
              'medium': ['квартиру', 'машину'],
              'high': ["квартиру и машину"]}