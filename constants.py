from system import load_image, load_clothes, load_buttons_images
from pygame.font import Font
from pygame import init

init()

BUTTONS = dict(load_buttons_images())
BUTTONS_ACTIVE = [load_image("alcoholic2.png", "/buttons"),
                  load_image("greedy2.png", "/buttons"),
                  load_image("angry2.png", "/buttons"),
                  load_image("irritable2.png", "/buttons"),
                  load_image("arrogant2.png", "/buttons"),
                  load_image("hypocrite2.png", "/buttons"),
                  load_image("selfish2.png", "/buttons"),
                  load_image("cruel2.png", "/buttons"),
                  load_image("lazy2.png", "/buttons"),
                  load_image("cheerful2.png", "/buttons"),
                  load_image("realist2.png", "/buttons"),
                  load_image("healthy2.png", "/buttons"),
                  load_image("generous2.png", "/buttons"),
                  load_image("kind2.png", "/buttons"),
                  load_image("calm2.png", "/buttons"),
                  load_image("modest2.png", "/buttons"),
                  load_image("rectilinear2.png", "/buttons"),
                  load_image("caring2.png", "/buttons"),
                  load_image("kind2.png", "/buttons"),
                  load_image("active2.png", "/buttons")]
BUTTONS_PASS = [load_image("alcoholic1.png", "/buttons"),
                load_image("greedy1.png", "/buttons"),
                load_image("angry1.png", "/buttons"),
                load_image("irritable1.png", "/buttons"),
                load_image("arrogant1.png", "/buttons"),
                load_image("hypocrite1.png", "/buttons"),
                load_image("selfish1.png", "/buttons"),
                load_image("cruel1.png", "/buttons"),
                load_image("lazy1.png", "/buttons"),
                load_image("cheerful1.png", "/buttons"),
                load_image("realist1.png", "/buttons"),
                load_image("healthy1.png", "/buttons"),
                load_image("generous1.png", "/buttons"),
                load_image("kind1.png", "/buttons"),
                load_image("calm1.png", "/buttons"),
                load_image("modest1.png", "/buttons"),
                load_image("rectilinear1.png", "/buttons"),
                load_image("caring1.png", "/buttons"),
                load_image("kind1.png", "/buttons"),
                load_image("active1.png", "/buttons")]
IMAGES = {'line_slider': load_image('line_slider.png'),
          'cursor': load_image('cursor.png'),
          'slider': load_image('slider.png'),
          'field': load_image('field.png'),
          'woman': load_image('woman.png')}
FONTS = {'Pacifico-Regular-60': Font('data/fonts/Pacifico-Regular.ttf', 60),
         'Pacifico-Regular-30': Font('data/fonts/Pacifico-Regular.ttf', 30),
         'RammettoOne-Regular-90': Font("data/fonts/RammettoOne-Regular.ttf", 90),
         'Standard-35': Font(None, 35)}

FACES = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('faces.txt')))
HAIRS = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('hairs.txt')))
BODIES = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('T-shirts.txt')))
PANTS = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('pants.txt')))

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
