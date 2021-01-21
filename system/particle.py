import os
import sys
import pygame
import random

screen_rect = (0, 0, 1920, 1080)


def load_image(name, path='', colorkey=None):
    fullname = os.path.join(f'{path}', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Particle(pygame.sprite.Sprite):
    def __init__(self, group, pos, dx, dy, image):
        super().__init__(group)

        img = load_image(image)
        fire = []
        for scale in (7, 8, 9):
            fire.append(pygame.transform.scale(img, (scale, scale)))

        self.image = random.choice(fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.5

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(groups, position, image):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(groups, position, random.choice(numbers), random.choice(numbers), image)


# Ввиду оптимизации данное графическое новшество было отключено.
# Мин требования: RTX 3080, IntelCore I7-10850 :3
