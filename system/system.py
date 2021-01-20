from pygame import quit, image as Image
from os.path import isfile, join
from os import listdir
from sys import exit


# Функция завершения игры
def terminate():
    quit()
    exit()


# Функция загрузки картинки
def load_image(name, path='', colorkey=None):
    fullname = join(f'data/images{path}', name)
    if not isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = Image.load(fullname)
    return image


# Функция загрузки списка одежды из файла
def load_clothes(name):
    fullname = join('./data/lists_clothes', name)
    if not isfile(fullname):
        print(f"Файл с одеждой '{fullname}' не найден")
        exit()
    with open(fullname, 'r', encoding='utf8') as file:
        path = file.readline().rstrip()
        lines = map(lambda x: (path, x.rstrip()), file.readlines())
    return list(lines).copy()


def load_buttons_images():
    path = './data/images/buttons'
    names = [(name[:-4], name) for name in listdir(path) if name[-3:] == 'png']
    return [(key, load_image(value, '/buttons')) for key, value in names]


def print_text(screen, pos_x, pos_y, text, color, font):
    string_rendered = font.render(text, 1, color)
    intro_rect = string_rendered.get_rect()
    intro_rect.top, intro_rect.x = pos_y, pos_x
    screen.blit(string_rendered, intro_rect)
