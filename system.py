from pygame import quit, image as Image
from os.path import isfile, join
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
    fullname = join(f'data/lists_clothes', name)
    if not isfile(fullname):
        print(f"Файл с одеждой '{fullname}' не найден")
        exit()
    with open(fullname, 'r', encoding='utf8') as file:
        path = file.readline().rstrip()
        lines = map(lambda x: (path, x.rstrip()), file.readlines())
    return list(lines).copy()