from system.system import load_image, load_clothes, load_buttons_images
from pygame.font import Font
from pygame import init

init()

BUTTONS = dict(load_buttons_images())
SCROLL_BUTTONS_ACTIVE = ['alcoholic2', 'greedy2', 'angry2', 'irritable2', 'arrogant2', 'hypocrite2', 'selfish2',
                         'lazy2', 'healthy2', 'generous2', 'kind2', 'calm2',
                         'modest2', 'rectilinear2', 'caring2', 'active2']

SCROLL_BUTTONS_PASS = ['alcoholic1', 'greedy1', 'angry1', 'irritable1', 'arrogant1', 'hypocrite1', 'selfish1',
                       'lazy1', 'healthy1', 'generous1', 'kind1', 'calm1',
                       'modest1', 'rectilinear1', 'caring1', 'active1']

IMAGES = {'line_slider': load_image('line_slider.png', '/other'),
          'cursor': load_image('cursor.png', '/other'),
          'slider': load_image('slider.png', '/other'),
          'field': load_image('field.png', '/other'),
          'woman': load_image('woman.png', '/other'),
          'scrollslider': load_image('scroll_slider.png', '/other'),
          'heart': load_image('heart.png', '/other'),
          'para': load_image('para2.png', '/other'),
          'win': load_image('win.png', '/other'),
          'lose': load_image('lose.png', '/other'),
          'authors': load_image('authors.png', '/other'),
          'arrow_down': load_image('arrow_down.png', '/other'),
          'arrow_up': load_image('arrow_up.png', '/other'),
          'stick': load_image('stick.png', '/other')}
FONTS = {'Pacifico-Regular-60': Font('./data/fonts/Pacifico-Regular.ttf', 60),
         'Pacifico-Regular-30': Font('./data/fonts/Pacifico-Regular.ttf', 30),
         'RammettoOne-Regular-90': Font('./data/fonts/RammettoOne-Regular.ttf', 90),
         'Standard-35': Font(None, 35)}

FACES = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('faces.txt')))
HAIRS = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('hairs.txt')))
BODIES = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('T-shirts.txt')))
PANTS = list(map(lambda x: (load_image(x[1], x[0]), x), load_clothes('pants.txt')))

CHARACTERS = [('алкаголик', 'ЗОЖник'), ('жадный', 'щедрый'), ('злобный', 'добрый'), ('раздрожительный', 'спокойный'),
              ('высокомерный', 'скромный'), ('лицимер', 'прямолинейный'), ('эгоистиченый', 'заботливый'),
              ('ленивый', 'активный')]

CHARACTERS_DICT = dict([(value, key) for key, value in CHARACTERS] + CHARACTERS)
CHARACTERS_LIST = ['алкаголик', 'жадный', 'злобный', 'раздрожительный', 'высокомерный', 'лицимер', 'эгоистиченый',
                   'ленивый', 'ЗОЖник', 'щедрый', 'добрый', 'спокойный',
                   'скромный', 'прямолинейный', 'заботливый', 'активный', 'добрый']

NAMES = ['Иван', 'Артём', 'Влад', 'Женя', 'Никита', 'Виталик', 'Петя', 'Жора', 'Гена', 'Роберт', 'Тимур', 'Саша',
         'Миша', 'Лёша', 'Алан', 'Вова', 'Богдан', 'Армэн', 'Олег', 'Ян', 'Иосиф', 'Денис', 'Слава', 'Артур', 'Рик',
         'Карэн', 'Альберт', 'Дима', 'Лев', 'Стас', 'Самуэль', 'Джон', 'Павел', 'Сава', 'Стёпа', 'Рэн', 'Рустам']

JOBS = {-2: ['никем', 'дворником', 'в макдональдсе', 'уборщиком', 'грузчиком', 'промоутер'],
        -1: ['учителем', 'врачом', 'сантехником', 'клоун', 'провизор', 'аптекарь'],
        1: ['строителем', 'мелким предпринимателем', 'инженером', 'электриком', 'пилотом'],
        2: ['бизнессмеом', 'нефтяником', 'банкиром', 'айтишником']}
JOBS = {value: key for key in JOBS.keys() for value in JOBS[key]}
PROPERTIES = {-2: ['ничего'],
              -1: ['хорошее чувство юмора'],
              1: ['квартиру', 'машину'],
              2: ["квартиру и машину"]}
PROPERTIES = {value: key for key in PROPERTIES.keys() for value in PROPERTIES[key]}
