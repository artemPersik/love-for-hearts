from system import load_image, load_clothes, load_buttons_images
from pygame.font import Font
from pygame import init

init()

BUTTONS = dict(load_buttons_images())
SCROLL_BUTTONS_ACTIVE = ['alcoholic2', 'greedy2', 'angry2', 'irritable2', 'arrogant2', 'hypocrite2', 'selfish2',
                         'cruel2', 'lazy2', 'cheerful2', 'realist2', 'healthy2', 'generous2', 'kind2', 'calm2',
                         'modest2', 'rectilinear2', 'caring2', 'kind2', 'active2']

SCROLL_BUTTONS_PASS = ['alcoholic1', 'greedy1', 'angry1', 'irritable1', 'arrogant1', 'hypocrite1', 'selfish1',
                       'cruel1', 'lazy1', 'cheerful1', 'realist1', 'healthy1', 'generous1', 'kind1', 'calm1',
                       'modest1', 'rectilinear1', 'caring1', 'kind1', 'active1']

IMAGES = {'line_slider': load_image('line_slider.png'),
          'cursor': load_image('cursor.png'),
          'slider': load_image('slider.png'),
          'field': load_image('field.png'),
          'woman': load_image('woman.png'),
          'scrollslider': load_image('scroll_slider.png'),
          'heart': load_image('heart.png'),
          'para': load_image('para2.png'),
          'win': load_image('win.png'),
          'lose': load_image('lose.png'),
          'authors': load_image('authors.png')}
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
