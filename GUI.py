import pygame


# Группа для всех спрайтов, с выводом слайдера и курсора поверх других изображений
class AllSprites(pygame.sprite.Group):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        sprites.sort(key=lambda x: isinstance(x, Slider))
        sprites.sort(key=lambda x: isinstance(x, Cursor))
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


# Клас курсора, ничего интересного)))
class Cursor(pygame.sprite.Sprite):
    def __init__(self, groups, image):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.groups = groups

    def update(self):
        if pygame.mouse.get_focused():
            self.rect.x, self.rect.y = pygame.mouse.get_pos()

        for group in self.groups:
            if self not in group:
                group.add(self)


# Класс кнопки
class Button(pygame.sprite.Sprite):
    # Ну тут тупа генератор, по названию переменных всё очевидно)
    def __init__(self, pos_x, pos_y, width, height, pass_image, direct_image, clicked_image,
                 groups, cursor, func, is_visible=True):
        super().__init__(*groups)

        self.pass_image = pygame.transform.scale(pass_image, (width, height))
        self.direct_image = pygame.transform.scale(direct_image, (width, height))
        self.clicked_image = pygame.transform.scale(clicked_image, (width, height))
        self.image = self.pass_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_visible = is_visible
        self.groups = groups
        self.pos = (pos_x, pos_y)
        self.cursor = cursor
        self.func = func
        self.width, self.height = width, height

    # Ну типа проверка нажатий и наведений на кнопку
    def update(self, *events):
        if not self.is_visible:
            return

        # проверка на на отпускае мыши
        if events and self.is_mouse_button_up(events[0]):
            self.image = self.clicked_image
            if self.func is not None:
                self.func()
        # проверка на нажатие мыши
        elif self.is_mouse_button_down():
            self.image = self.clicked_image
        # проверка на наведение мыши на кнопку
        elif self.is_direct():
            self.image = self.direct_image
        else:
            self.image = self.pass_image

    # Проверка на на отпускае мыши
    def is_direct(self):
        return not pygame.mouse.get_pressed(3)[0] and pygame.sprite.collide_mask(self, self.cursor)

    # Проверка на нажатие мыши
    def is_mouse_button_down(self):
        return pygame.mouse.get_pressed(3)[0] and pygame.sprite.collide_mask(self, self.cursor)

    # Проверка на на отпускае мыши
    def is_mouse_button_up(self, event):
        return event.type == pygame.MOUSEBUTTONUP and event.button == 1 and pygame.sprite.collide_mask(self, self.cursor)

    # Куча методов для изменения и получения переменных экземпляра класса
    def get_pos(self):
        return self.pos

    def get_pos_x(self):
        return self.pos[0]

    def get_pos_y(self):
        return self.pos[1]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_func(self):
        return self.func

    def set_pass_image(self, image):
        self.pass_image = image

    def set_direct_image(self, image):
        self.direct_image = image

    def set_clicked_image(self, image):
        self.clicked_image = image

    def set_pos(self, pox_x, pos_y):
        self.pos = (pox_x, pos_y)
        self.rect.x, self.rect.y = self.get_pos()

    def set_width(self, width):
        self.width = width
        self.rect.width = self.get_width()

    def set_height(self, height):
        self.height = height
        self.rect.height = self.get_height()

    def set_func(self, func):
        self.func = func

    def set_visible(self, value):
        if value and all(self not in group for group in self.groups):
            for group in self.groups:
                group.add(self)
        if not value and all(self in group for group in self.groups):
            for group in self.groups:
                group.remove(self)


# Класс для ползунка у слайдера
class Slider(pygame.sprite.Sprite):
    def __init__(self, image, groups, size=None):
        super().__init__(*groups)
        if size is not None:
            image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect()
        self.groups = groups


# Класс для слайдера громкостти
class VolumeSlider(pygame.sprite.Sprite):
    def __init__(self, pos, line_image, line_size, size, slider, groups, volume):
        super().__init__(*groups)
        self.image = pygame.transform.scale(line_image, line_size)
        self.rect = self.image.get_rect().move(pos[0], pos[1] + (size[1] - line_size[1]) // 2)
        self.volume_slider = pygame.Rect(*pos, *size)
        self.slider, self.volume, self.flag = slider, volume, False
        self.slider.rect.x, self.slider.rect.y = size[0] * volume + pos[0] - slider.rect.width // 2, pos[1]

        self.groups = groups
        self.pos_x, self.pos_y = pos
        self.width, self.height = size
        self.slider_width, self.slider_height = self.rect.size

    # Метод для того, чтобы ползунок не уходил дальше положенного
    def fix_slider_coord(self):
        if self.slider.rect.x < self.rect.x - self.slider.rect.width // 2:
            self.slider.rect.x = self.rect.x - self.slider.rect.width // 2
        elif self.slider.rect.x > self.rect.x + self.rect.width - self.slider.rect.width // 2:
            self.slider.rect.x = self.rect.x + self.rect.width - self.slider.rect.width // 2

    # Метод для движения ползунка по слайдеру
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.volume_slider.collidepoint(event.pos):
            self.slider.rect.x = event.pos[0] - self.slider.rect.width // 2
            self.flag = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.flag = False

        if event.type == pygame.MOUSEMOTION and self.flag:
            self.slider.rect.x += event.rel[0]
            self.fix_slider_coord()

        if event.type == pygame.MOUSEWHEEL:
            self.slider.rect.x += event.y * self.slider.rect.width // 20
            self.fix_slider_coord()
        self.volume = round((self.slider.rect.x - self.rect.x + self.slider.rect.width // 2) / self.rect.width, 2)

    # Метод для получения громкости
    def get_volume(self):
        return self.volume

